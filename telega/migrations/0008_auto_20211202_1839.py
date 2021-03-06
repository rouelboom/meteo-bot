# Generated by Django 3.2.9 on 2021-12-02 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telega', '0007_auto_20211201_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeteoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(verbose_name='temperature')),
                ('humidity', models.FloatField(verbose_name='humidity')),
            ],
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='phone_number',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
