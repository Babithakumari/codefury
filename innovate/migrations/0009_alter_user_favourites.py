# Generated by Django 4.1 on 2022-08-13 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innovate', '0008_remove_user_favourites_user_favourites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favourites',
            field=models.ManyToManyField(blank='True', null='True', related_name='favourites', to='innovate.startup'),
        ),
    ]
