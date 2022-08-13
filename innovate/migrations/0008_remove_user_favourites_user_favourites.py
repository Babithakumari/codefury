# Generated by Django 4.1 on 2022-08-13 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innovate', '0007_user_favourites_delete_favourite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favourites',
        ),
        migrations.AddField(
            model_name='user',
            name='favourites',
            field=models.ManyToManyField(blank='True', null='True', related_name='favourited_by', to='innovate.startup'),
            preserve_default='True',
        ),
    ]
