from django.db import models
from django.contrib.auth.models import User


class PersonalData(models.Model):
    """
    Stores additional data, related to one User object.
    Holds string of wrong words to use in searching.
    """
    user = models.OneToOneField(User)
    wrong_words = models.TextField()