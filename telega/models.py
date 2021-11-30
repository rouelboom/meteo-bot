from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Things(models.Model):

    some = models.IntegerField(verbose_name='something')


class TelegramUser(models.Model):
    """
    All the users of bot
    """
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telega_user')
    user_telega_id = models.IntegerField(verbose_name='user_telegram_unique_id', unique=True)
    username = models.CharField(verbose_name='username', max_length=150)
    first_name = models.CharField(verbose_name='first_name', max_length=150)
    creation_date = models.DateTimeField(verbose_name='creation_date')
    last_login_date = models.DateTimeField(verbose_name='creation_date')
