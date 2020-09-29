from django.contrib.auth.models import AbstractUser
from django.db import models

# Do I need this?
class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=256)


# TO-DO: mess with this for next specs.
class listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    high_bidder = models.ForeignKey('User', related_name='bidder', on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.URLField()
    category = models.CharField(max_length=64)
    owner = models.ForeignKey('User', related_name='listing_owner', on_delete=models.CASCADE, blank=True, null=True)
