# Generated by Django 4.0.4 on 2023-08-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('isactive', models.BooleanField(default=True)),
                ('winner', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='auction_user',
        ),
    ]
