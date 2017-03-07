from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class StringText(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text

class PersonalData(models.Model):
    user = models.OneToOneField(User)
    bad_words = models.TextField()