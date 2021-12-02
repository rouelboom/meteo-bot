from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Things(models.Model):
    some = models.IntegerField(verbose_name='something')


class MeteoData(models.Model):
    temperature = models.FloatField(verbose_name='temperature')
    humidity = models.FloatField(verbose_name='humidity')


class TelegramUser(models.Model):
    """
    All the users of bot
    """
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telega_user')
    user_telega_id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(verbose_name='username', max_length=150, null=True)
    first_name = models.CharField(verbose_name='first_name', max_length=150)
    creation_date = models.DateTimeField(verbose_name='creation_date')
    last_login_date = models.DateTimeField(verbose_name='creation_date')
    ban = models.BooleanField(verbose_name='ban', default=False)
    temp_block = models.BooleanField(default=False, null=True)
    bad_date = models.DateTimeField(null=True)
    temp_block_date = models.DateTimeField(null=True)
    phone_number = models.CharField(null=True, max_length=30)
