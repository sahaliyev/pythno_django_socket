from django.contrib.auth.models import User
from django.db import models


class UploadImage(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='owner')
    title = models.CharField(max_length=400)
    image = models.ImageField(upload_to='images')
    thumbnails = models.ImageField(upload_to='thumbnails', editable=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='comment_owner')
    post = models.ForeignKey(UploadImage, on_delete=models.CASCADE)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.comment


class SharedPost(models.Model):
    image = models.ForeignKey(UploadImage, blank=True, on_delete=models.CASCADE)
    person = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    write_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.image.title