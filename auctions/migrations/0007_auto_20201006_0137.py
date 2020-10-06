# Generated by Django 3.1.1 on 2020-10-06 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201005_0034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='Active',
            new_name='active',
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