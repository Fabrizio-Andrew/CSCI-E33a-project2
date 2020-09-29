from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# TO-DO: mess with this for next specs.
class listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    bid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#   TO-DO: implement many-to-many association for high-bidder
#    high_bidder = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.URLField()
    category = models.CharField(max_length=64)
#   TO-DO record authenticated user and send here.
    owner = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
