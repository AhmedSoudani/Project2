# Generated by Django 4.0.4 on 2023-08-01 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_image_alter_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='image',
            new_name='image_URL',
        ),
    ]
