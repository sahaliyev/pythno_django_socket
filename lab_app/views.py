import os
import pdb

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import UploadImageForm
from .forms import UserForm
from .models import Comments
from .models import SharedPost
from .models import UploadImage
from .tasks import resize_image_task


class IndexView(View):
    template_name = 'index/index.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'auth/register.html'

    def get(self, request):
        context = {}
        context['form'] = UserForm(None)
        try:
            email = request.session['email']
        except:
            email = None

        if email is None:
            return render(request, self.template_name, context)
        else:
            return redirect('/')

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password)
            messages.success(request, 'User successfully created!')
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request):
        try:
            email = request.session['email']
        except:
            email = None

        if email is None:
            return render(request, self.template_name)
        else:
            return redirect('/')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = None

        if user:
            if user.check_password(password):
                request.session['email'] = email
                request.session['id'] = user.pk
                request.session['full_name'] = user.first_name + ' ' + user.last_name
                messages.success(
                    request, "You successfully logged in!"
                )
                return redirect('/')

            messages.error(
                request, "Password is not correct!"
            )
            return render(request, self.template_name)

        messages.error(
            request, "Username is not correct!"
        )
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        request.session.flush()

        return redirect('/login')


class UploadImageView(View):
    template_name = 'upload_image/upload_image.html'

    def get(self, request):
        # print(request.session['email'])
        context = {}
        context['form'] = UploadImageForm(None)
        return render(request, self.template_name, context)

    def post(self, request):
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES.get('image')
            pending_object = form.save()
            image_path = os.path.join(settings.MEDIA_ROOT, 'images/' + image.name.replace(' ', '_'))
            user_name = request.session['email']
            thumb_path = 'thumb_' + image.name
            thumb_image_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails/' + thumb_path)
            resize_image_task.delay(image_path, thumb_image_path, pending_object.pk, user_name)

            messages.success(request, 'File successfully uploaded!')
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class YourImagesView(View):
    template_name = 'your_images/your_images.html'

    def get(self, request):
        user = User.objects.get(username=request.session['email'])
        images = UploadImage.objects.filter(user_id=user.id)
        args = {
            'images': images
        }
        return render(request, self.template_name, args)

    def post(self, request):
        post_id = request.POST.get('post_id')
        username = request.POST.get('username')
        permission = request.POST.get('permission')
        permission = True if int(permission) == 1 else False
        post_id = int(post_id)

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None

        if user:
            post = UploadImage.objects.get(pk=post_id)

            SharedPost.objects.create(image=post, person=user, write_permission=permission)
            return JsonResponse({"message": "Successfully shared!!!"})
        return JsonResponse({"message": "User with this username not found!"})


class ImageDetailsView(View):
    template_name = 'your_images/details.html'

    def get(self, request, post_id):
        user = User.objects.get(username=request.session['email']).id
        post = UploadImage.objects.get(pk=post_id)
        try:
            post_permission = SharedPost.objects.get(image_id=post_id).write_permission
        except:
            post_permission = None

        args = {
            'post': post,
            'permission': post_permission,
            'user': user,
        }
        return render(request, self.template_name, args)


class SharedWithYouView(View):
    template_name = 'shared_images/shared_with_you.html'

    def get(self, request):
        user_name = request.session['email']
        user = User.objects.get(username=user_name)
        shared_posts = SharedPost.objects.filter(person=user)

        args = {
            'shared_posts': shared_posts
        }
        return render(request, self.template_name, args)


class DeleteCommentView(View):
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        try:
            comment = Comments.objects.get(pk=comment_id)
        except ObjectDoesNotExist:
            comment = None
        if comment:
            comment.visible = False
            comment.save()
            return JsonResponse({"message": "Successfully deleted!!!"})
        return JsonResponse({"message": "Comment is not available!"})


class EditCommentView(View):
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        comment_text = request.POST.get('comment_text')
        try:
            comment = Comments.objects.get(pk=comment_id)
        except ObjectDoesNotExist:
            comment = None
        if comment:
            comment.comment = comment_text
            comment.save()
            return JsonResponse({"message": "Successfully edited!!!"})
        return JsonResponse({"message": "Comment is not available!"})