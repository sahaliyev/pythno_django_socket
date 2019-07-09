from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('upload_image/', views.UploadImageView.as_view(), name='upload_image'),
    path('your_images/', views.YourImagesView.as_view(), name='your_images'),
    path('details/<int:post_id>/', views.ImageDetailsView.as_view(), name='details'),
    path('shared_images/', views.SharedWithYouView.as_view(), name='shared_images'),
    path('delete_comment/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('edit_comment/', views.EditCommentView.as_view(), name='edit_comment'),
]
