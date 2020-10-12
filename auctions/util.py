from .models import Listing

def append_highbids(listings):
    """
    Gets the high bid for a listing (or a list of listings), appends the
    high bids to the listing objects, and returns the updated list.
    """
    results = []
    for listing in listings:
        listing.high_bid = Listing.high_bid(listing)
        results.append(listing)
    return results
