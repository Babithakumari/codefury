# Generated by Django 4.0.1 on 2022-08-13 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innovate', '0014_startup_business_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='images/profiles/'),
        ),
    ]