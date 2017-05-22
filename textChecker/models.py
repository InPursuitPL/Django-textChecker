from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PersonalData(models.Model):
    """
    Stores additional data, related to one User object.
    Holds string of wrong words to use in searching.
    """
    user = models.OneToOneField(User)
    wrong_words = models.TextField()

    def __str__(self):
        return "{}'s personal data".format(self.user)

    @receiver(post_save, sender=User)
    def create_user_personaldata(sender, instance, created, **kwargs):
        if created:
            PersonalData.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_personaldata(sender, instance, **kwargs):
        instance.personaldata.save()
