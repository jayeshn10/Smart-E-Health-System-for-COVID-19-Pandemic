# Generated by Django 3.2 on 2021-04-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_address',
            field=models.TextField(blank=True, null=True, verbose_name='Customer Address'),
        ),
    ]