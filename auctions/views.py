from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comments


def login_view(request):
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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def new_listing(request):
    return render(request, "auctions/create_listing.html")


def create_listing(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        newlisting = Listing(title=request.POST["title"],
                    starting_bid=request.POST["starting_bid"],
                    category=request.POST["category"],
                    image_url=request.POST["image_url"],
                    description=request.POST["description"],
                    owner=User.objects.get(pk=user_id),
                    active=True
        )
        newlisting.save()
        return HttpResponseRedirect(reverse("index"))

def listing_page(request, listing_name, user_id):
    listing = Listing.objects.get(title=f"{listing_name}")
    user = User.objects.get(pk=user_id)
    watchlist = user.watchlist.all()
    comments = Comments.objects.filter(listing=listing)
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "watchlist": watchlist,
        "user": user,
        "comments": comments
    })

def watch(request):
    """
    Handles adding/removing listings from user's watchlist.
    """
    if request.method == "POST":
        user = User.objects.get(pk=request.POST["user_id"])
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        return HttpResponseRedirect(f"/listing/{listing.title}/{user.id}")

def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })

def categories(request):
    categories = Listing.objects.values('category').distinct()
    for entry in categories:
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listing(request, category):
    return render(request, "auctions/category_listing.html", {
        "category": category,
        "listings": Listing.objects.filter(category=category)
    })

def add_comment(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        user = User.objects.get(pk=request.POST["user_id"])
        newcomment = Comments(author=user,
                    listing=listing,
                    body=request.POST["comment"]
        )
        newcomment.save()
    return HttpResponseRedirect(f"/listing/{listing.title}/{user.id}")
