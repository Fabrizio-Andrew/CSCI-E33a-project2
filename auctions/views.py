"""
Commerce Views Module

This module contains the functions that support all logic for addiing, removing,
updating, and displaying data associated with the Commerce app.
"""

from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comments, Bids
from .forms import NewListingForm, BidForm
from .util import append_highbids


def login_view(request):
    """
    Given a username and password via POST, authenticates the user via
    django.contrib.auth.authenticate.
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    """
    Logs out the current user.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Given a username, email, password, and pw confirmation, creates a new User
    object with the given credential.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def index(request):
    """
    For all objects in Listing, gets the highest bid amount from all related bid
    objects.  Appends "high_bid" to the listing object, and appends the updated
    listing object to a list called "listings".
    """
    return render(request, "auctions/index.html", {
        "listings": append_highbids(Listing.objects.filter(active=True))
    })


def new_listing(request):
    """
    Given the details of the user, listing, and starting bid for an item via POST,
    create instances of the Listing and Bids models to represent the item and
    starting bid.  Return redirect to index.

    For GET requests, render the create_listing form.
    """
    if request.method == "POST":
        user = User.objects.get(pk=request.POST["user_id"])
        newlisting = Listing(title=request.POST["title"],
                             category=request.POST["category"],
                             image_url=request.POST["image_url"],
                             description=request.POST["description"],
                             owner=user,
                             active=True,
                             starting_bid=request.POST["starting_bid"]
                             )
        newlisting.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })


def listing_page(request, listing_id, user_id):
    """
    Given a listing_id and user_id (if authenticated), return the related listing
    info, current bid, comments, and watchlist info as context for listing_page.html.
    """
    listing = Listing.objects.get(pk=listing_id)

    high_bid = Listing.high_bid(listing)
    if high_bid != 0:
        listing.high_bid = high_bid
    context = {
        "listing": listing,
        "comments": Comments.objects.filter(listing=listing),
        "form": BidForm()
    }
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        context['watchlist'] = user.watchlist.all()
        context['user'] = user
    return render(request, "auctions/listing_page.html", context)


def watch(request):
    """
    Given a user and listing via POST, adds/removes the listing from
    the user's watchlist.
    """
    if request.method == "POST":
        user = User.objects.get(pk=request.POST["user_id"])
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
    return HttpResponseRedirect(f"/listing/{listing.id}/{user.id}")


def watchlist(request, user_id):
    """
    Given a user, returns the user's watchlist as context for watchlist.html.
    """
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "listings":  append_highbids(user.watchlist.all())
    })


def categories(request):
    """
    Gets a list of distinct categories from the Listing table and provides list
    as context for categories.html.
    """
    return render(request, "auctions/categories.html", {
        "categories": Listing.objects.filter(active=True).values('category').distinct()
    })


def category_listing(request, category):
    """
    Given a category, returns a list of listings with in that category with associated
    high bid (if any) as context for category_listing.html.
    """
    listings = []
    for listing in Listing.objects.filter(category=category):
        if listing.active is True:
            listings.append(listing)
    return render(request, "auctions/index.html", {
        "category": category,
        "listings": append_highbids(listings)
    })


def add_comment(request):
    """
    Accepts data via POST to create a Comment object associated to a User and Listing.
    """
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        user = User.objects.get(pk=request.POST["user_id"])
        newcomment = Comments(author=user,
                              listing=listing,
                              body=request.POST["comment"]
                              )
        newcomment.save()
    return HttpResponseRedirect(f"/listing/{listing.id}/{user.id}")


def bid(request):
    """
    Accepts bida data via POST, determines if the new bid is >= starting bid
    and > high bid (if it exists), and creates the bid object as an instance of
    models.Bids.
    """
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        user = User.objects.get(pk=request.POST["user_id"])
        newbid_amount = Decimal(request.POST["bid_amount"])

        context = {
            "listing": listing,
            "comments": Comments.objects.filter(listing=listing),
            "watchlist": user.watchlist.all(),
            "user": user,
            "form": BidForm()
        }
        if newbid_amount > Listing.high_bid(listing) and newbid_amount >= listing.starting_bid:
            newbid = Bids(user=user,
                          listing=listing,
                          amount=newbid_amount,
                          )
            newbid.save()
            listing.high_bid = Listing.high_bid(listing)
            context['message'] = "Bid Accepted"
            return render(request, "auctions/listing_page.html", context)
        if Listing.high_bid != 0:
            listing.high_bid = Listing.high_bid(listing)
        context['message'] = "ERROR: Please increase your bid."
    return render(request, "auctions/listing_page.html", context)


def close(request):
    """
    Given a listing and user via POST, if the user is the owner of the listing,
    set listing.active to False and listing.winner to the current high bidder.
    """
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        user = User.objects.get(pk=request.POST["user_id"])
        if user == listing.owner:
            listing.active = False
            if Bids.objects.filter(listing=listing):
                listing.winner = Bids.objects.filter(listing=listing).order_by('-amount')[0].user
            listing.save(update_fields=['active', 'winner'])
    return HttpResponseRedirect(f"/listing/{listing.id}/{user.id}")


def my_wins(request, user_id):
    """
    Renders a list of auctions the user has won on my_wins.html.
    """
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/my_wins.html", {
        "listings": Listing.objects.filter(winner=user)
    })
