from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
