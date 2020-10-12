"""
Commerce Data Models:
This module outlines 4 modules: User, Listing, Bids, and Comments.

Models are configured to configure a sqlite database titled db.sqlite3.
Before running the app, this document must be established via the following shell commands:
$ python manage.py makemigrations
$ python manage.py migrate
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Contains all data regarding users & accounts.
    """
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    watchlist = models.ManyToManyField(
        'Listing',
        blank=True,
        related_name='watchlist'
    )
    bids = models.ManyToManyField(
        'Listing',
        through='Bids',
        through_fields=('user', 'listing'),
        related_name='bids'
    )

    def __str__(self):
        return f"<{self.pk}: {self.username}>"

    class Meta:
        """
        Contains name info about User class to be displayed on Django admin.

        Please note: pylint returns the error "Too few public methods".  However,
        this class has been implemented correctly according to Django's documentation
        at: https://docs.djangoproject.com/en/3.1/ref/models/options/.
        """
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Listing(models.Model):
    """
    Contains all data pertaining to auction listings.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image_url = models.URLField(blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=64)
    active = models.BooleanField()
    bidders = models.ManyToManyField(
        'User',
        through='Bids',
        through_fields=('listing', 'user'),
        related_name='bidders'
    )
    owner = models.ForeignKey(
        'User',
        related_name='listing_owner',
        on_delete=models.CASCADE
    )
    winner = models.ForeignKey(
        'User',
        related_name='listing_winner',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"<{self.pk}: {self.title}"

    class Meta:
        """
        Contains name info about Listing class to be displayed on Django admin.

        Please note: pylint returns the error "Too few public methods".  However,
        this class has been implemented correctly according to Django's documentation
        at: https://docs.djangoproject.com/en/3.1/ref/models/options/.
        """
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def high_bid(self):
        """
        Returns the amount of the highest bid on a particular Listing.

        Please note: pylint returns the error "Class 'Bids' has no 'objects' member."  However,
        this is because the 'Bids' is a subclass of the 'Model' class and inherits 'objects'
        from it.
        """
        if Bids.objects.filter(listing=self):
            return Bids.objects.filter(listing=self).order_by('-amount')[0].amount
        return 0


class Bids(models.Model):
    """
    Contains data related to Bids by users on specific listings.
    """
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'User',
        related_name='bidder',
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        'Listing',
        related_name='listing_bid',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"<{self.pk}: {self.amount} on {self.listing} by {self.user}>"

    class Meta:
        """
        Contains name info about Bids class to be displayed on Django admin.

        Please note: pylint returns the error "Too few public methods".  However,
        this class has been implemented correctly according to Django's documentation
        at: https://docs.djangoproject.com/en/3.1/ref/models/options/.
        """
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'


class Comments(models.Model):
    """
    Contains all data pertaining to comments left by users on listings.
    """
    body = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'User',
        related_name='author',
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        'Listing',
        related_name='listing_comment',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"<{self.pk}: {self.author} comment on {self.listing}>"

    class Meta:
        """
        Contains name info about Comments class to be displayed on Django admin.

        Please note: pylint returns the error "Too few public methods".  However,
        this class has been implemented correctly according to Django's documentation
        at: https://docs.djangoproject.com/en/3.1/ref/models/options/.
        """
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
