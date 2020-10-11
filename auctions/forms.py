from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2)
    Category = forms.CharField(max_length=64)
    image_url = forms.URLField()
    description = forms.CharField(widget=forms.Textarea, max_length=500)

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=8, decimal_places=2)