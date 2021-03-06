# Generated by Django 3.1.1 on 2020-10-06 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20201006_0137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='comments',
        ),
        migrations.AlterField(
            model_name='comments',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bids',
            field=models.ManyToManyField(related_name='bids', through='auctions.Bids', to='auctions.Listing'),
        ),
        migrations.AlterField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to='auctions.Listing'),
        ),
    ]
