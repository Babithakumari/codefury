# Generated by Django 4.1 on 2022-08-13 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innovate', '0009_alter_user_favourites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favourites',
            field=models.ManyToManyField(to='innovate.startup'),
        ),
    ]