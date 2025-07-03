from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField('Имя пользователя', max_length=200, unique=True, null=False, blank=False)
    password = models.CharField('Пароль', max_length=100, null=False, blank=False)