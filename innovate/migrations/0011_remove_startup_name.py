# Generated by Django 4.1 on 2022-08-13 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('innovate', '0010_alter_user_favourites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='startup',
            name='name',
        ),
    ]
