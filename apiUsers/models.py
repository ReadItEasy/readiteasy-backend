from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # title = models.CharField(max_length=5)
    # dob = models.DateField()
    # address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    mandarin_known_words = models.TextField(blank=True, default='')
    mandarin_study_words = models.TextField(blank=True, default='')
    english_known_words = models.TextField(blank=True, default='')
    english_study_words = models.TextField(blank=True, default='')

    # city = models.CharField(max_length=50)
    # zip = models.CharField(max_length=5)
    # photo = models.ImageField(upload_to='uploads', blank=True)