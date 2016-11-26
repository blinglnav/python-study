from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=256)
    encrypted_password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)
    encrypt_cycle = models.IntegerField(default=25000)
    is_valid = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
