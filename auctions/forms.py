"""
Commerce Forms Module:

Contains form classes to collect & validate info.
"""

from django import forms

class NewListingForm(forms.Form):
    """
    Form class to collect info necessary to create a new listing.
    """
    title = forms.CharField(max_length=64)
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2)
    category = forms.CharField(max_length=64)
    image_url = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=500)

class BidForm(forms.Form):
    """
    Form class to collect and validate a bid from a user.
    """
    bid_amount = forms.DecimalField(max_digits=8, decimal_places=2)