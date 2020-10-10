from .models import Bids

def high_bid(listing):
    if Bids.objects.filter(listing=listing):
        return Bids.objects.filter(listing=listing).order_by('amount')[0].amount
    return 0