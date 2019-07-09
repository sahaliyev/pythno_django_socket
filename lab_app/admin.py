from django.contrib import admin

from .models import Comments
from .models import UploadImage
from .models import SharedPost
# Register your models here.

admin.site.register(UploadImage)
admin.site.register(Comments)
admin.site.register(SharedPost)
