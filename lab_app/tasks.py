import os
from datetime import datetime
from django.contrib.auth.models import User

from PIL import Image
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files import File

from .models import UploadImage

logger = get_task_logger(__name__)


@shared_task
def resize_image_task(image_path, thumb_image_path, id, user_name):
    logger.info('started resize_image_task function at time {0}'.format(datetime.now()))
    pending_object = UploadImage.objects.get(pk=id)
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.ANTIALIAS)
    image.save(thumb_image_path)
    pending_object.thumbnails = File(open(thumb_image_path, 'rb'))
    pending_object.thumbnails.name = pending_object.thumbnails.name[61:]
    pending_object.user = User.objects.get(username=user_name)
    pending_object.save()

    try:
        os.remove(thumb_image_path)
    except:
        pass
