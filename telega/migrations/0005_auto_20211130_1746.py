# Generated by Django 3.2.9 on 2021-11-30 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telega', '0004_rename_telegramusers_telegramuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='user_telegra_id',
            field=models.IntegerField(default=274484976, unique=True, verbose_name='user_telegram_unique_id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first_name'),
        ),
    ]