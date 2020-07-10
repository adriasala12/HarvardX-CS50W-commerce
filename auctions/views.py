from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from django.db.models import Max


def index(request):

    for i in Listing.objects.all():
        bids = list(i.bids.all())

        if bids.count != 0:
            i.base_price = i.bids.all().aggregate(Max('price')).get('price__max')
            i.save()

    context = {
        "listings": Listing.objects.filter(is_active=True),
    }

    return render(request, "auctions/index.html", context)


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing does not exist")

    listing.base_price = listing.bids.all().aggregate(Max('price')).get('price__max')
    listing.save()

    ###### CONTINUE HERE ######
    ###########################
    print(listing.user.watchlist.all())


    context = {
        "listing": listing,
        "winner": listing.bids.filter(price=listing.base_price).first().user
    }

    return render(request, "auctions/listing.html", context)


def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_price = int(request.POST.get('bid_price'))

    b = Bid(price=bid_price, listing=listing, user=request.user)
    b.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


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
