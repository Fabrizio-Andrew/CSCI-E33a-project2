from django.contrib.auth.models import AbstractUser
from django.db import models

# Do I need this?
class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchlist')
    bids = models.ManyToManyField('Listing', through='Bids', through_fields=('user', 'listing'), related_name='bids')

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    bidders = models.ManyToManyField('User', through='Bids', through_fields=('listing', 'user'), related_name='bidders')
    image_url = models.URLField()
    category = models.CharField(max_length=64)
    owner = models.ForeignKey('User', related_name='listing_owner', on_delete=models.CASCADE)
    active = models.BooleanField()

class Bids(models.Model):
    user = models.ForeignKey('User', related_name='bidder', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', related_name='listing_bid', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    author = models.ForeignKey('User', related_name='author', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', related_name='listing_comment', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
