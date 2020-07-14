from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment
from django.db.models import Max
from django.forms import modelform_factory


def index(request):

    context = {
        "listings": Listing.objects.filter(is_active=True),
    }

    return render(request, "auctions/index.html", context)


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing does not exist")

    if listing in listing.user.watchlist.all():
        is_in_watchlist = True
    else:
        is_in_watchlist = False

    try:
        winner = listing.bids.filter(price=listing.base_price).first().user
    except:
        winner = None

    context = {
        "listing": listing,
        "category": listing.category,
        "winner": winner,
        "is_in_watchlist": is_in_watchlist,
    }

    return render(request, "auctions/listing.html", context)


def categories(request):

    dic = dict()
    listings = list(Listing.objects.all())

    for category in Listing.CATEGORIES:
        dic[category[0]] = list(filter(lambda l: l.category==category[0], listings))

    context = {
        "categories": dic,
    }

    return render(request, "auctions/categories.html", context)


@login_required(login_url='login')
def add_watchlist(request, listing_id):

    watchlist = request.user.watchlist
    listing = Listing.objects.get(pk=listing_id)

    if listing in listing.user.watchlist.all():
        watchlist.remove(listing)
    else:
        watchlist.add(listing)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url='login')
def watchlist(request):

    context = {
        "listings": request.user.watchlist.all()
    }

    return render(request, "auctions/watchlist.html", context)


@login_required(login_url='login')
def add_listing(request):

    if request.method == 'POST':

        r = request.POST

        if r['is_active'] == 'on':
            state = True
        else:
            state = False

        Listing.objects.create(
            name = r['name'],
            base_price = float(r['base_price']),
            description = r['description'],
            user = request.user,
            image_url = r['image_url'],
            is_active = state,
            category = r['category']
        )

        return HttpResponseRedirect(reverse("index"))

    listing_form = modelform_factory(Listing, exclude=['user'])

    return render(request, "auctions/create.html", {'form': listing_form})


@login_required(login_url='login')
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_price = float(request.POST.get('bid_price'))

    b = Bid(price=bid_price, listing=listing, user=request.user)
    listing.base_price = bid_price
    b.save()
    listing.save()

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
