from django.db import models
from django.conf import settings
from django.utils import timezone
from .lang_choices import LANG_CHOICES
# Create your models here.

class AudioFile(models.Model):
    id = models.AutoField(primary_key=True)
    upload_file = models.FileField(upload_to=settings.MEDIA_ROOT)
    language = models.TextField(choices=LANG_CHOICES,default='fr-FR')
    name = models.CharField(max_length=200,default='Sans titre')
    add_date = models.DateTimeField('Added Date',auto_now_add=True)
    
class TextFile(models.Model):
    audiofile = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    text_file = models.TextField(max_length=4000)
    name = models.CharField(max_length=200)
