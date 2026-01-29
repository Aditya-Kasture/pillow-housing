from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    school = models.CharField(max_length=200, blank=True)
    grad_year = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.email or self.username