"""
Commerce Util Module

This module contains functions that are consumed by multiple views.py methods,
but don't necessarily belong within a particular model.  (Right now, it's just
append_highbids)
"""

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
