from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Category, Auction_Listing, Bid, Comment
from .forms import NewListingForm, NewBidForm, AddCommentForm

import logging
logger = logging.getLogger(__name__)


def index(request):
    # listings = Auction_Listing.objects.all()
    listings = Auction_Listing.objects.filter(closed=False)
    arr = []
    for x in listings:
        b = Bid.objects.filter(listing=int(x.pk)).last()
        arr.append(b)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "array": arr
    })


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


def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            url_image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            created_by = User.objects.get(pk=int(request.user.pk))
            a = Auction_Listing(title=title, description=description,
                                starting_bid=starting_bid, url_image=url_image, category=category,
                                created_by=created_by, closed=False)
            a.save()

    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })


def listing(request, listing_id):
    # comments = Comment.objects.filter(listing=int(listing_id))
    comments = Comment.objects.filter(listing=int(listing_id))
    listing = Auction_Listing.objects.get(pk=int(listing_id))

    try:
        bids = Bid.objects.filter(listing=int(listing_id)).last()

    except Bid.DoesNotExist:
        bids = None
    if request.method == "POST":
        if 'add_watchlist' in request.POST:
            user = User.objects.get(pk=int(request.user.pk))
            user.watchlist.add(listing)
        elif 'remove_watchlist' in request.POST:
            user = User.objects.get(pk=int(request.user.pk))
            user.watchlist.remove(listing)
        elif 'close_auction' in request.POST:
            listing.closed = True
            listing.save()
        elif 'add_comment' in request.POST:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment_title = form.cleaned_data['comment_title']
                comment = form.cleaned_data['comment']
                commenter = User.objects.get(pk=int(request.user.pk))
                c = Comment(comment_title=comment_title, comment=comment, listing=listing,
                            commenter=commenter)
                c.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "bid_form": NewBidForm(),
        "bid_submit": False,
        "comments": comments,
        "comment_form": AddCommentForm()
    })


def bid_submit(request, listing_id):
    comments = Comment.objects.filter(listing=int(listing_id))
    listing = Auction_Listing.objects.get(pk=int(listing_id))
    user = User.objects.get(pk=int(request.user.pk))
    currentBid = Bid.objects.filter(listing=listing).last()
    try:
        bids = Bid.objects.filter(listing=int(listing_id)).last()

    except Bid.DoesNotExist:
        bids = None

    if request.method == "POST":

        bidForm = NewBidForm(request.POST)
        if bidForm.is_valid():
            bid = bidForm.cleaned_data['bid']

            if bid < listing.starting_bid:
                error = f"The bid needs to be larger than the current bid and the starting bid."
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_form": NewBidForm(),
                    "error_message": error,
                    "bids": bids,
                    "bid_submit": False,
                    "comments": comments,
                    "comment_form": AddCommentForm()
                })
            elif bid > listing.starting_bid and currentBid is None:
                b = Bid(bid=bid, listing=listing, user=user)
                b.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_form": NewBidForm(),
                    "bids": Bid.objects.filter(listing=int(listing_id)).last(),
                    "bid_submit": True,
                    "comments": comments,
                    "comment_form": AddCommentForm()
                })

            elif bid > currentBid.bid and bid > listing.starting_bid:
                b = Bid(bid=bid, listing=listing, user=user)
                b.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_form": NewBidForm(),
                    "bids": Bid.objects.filter(listing=int(listing_id)).last(),
                    "bid_submit": True,
                    "comments": comments,
                    "comment_form": AddCommentForm()
                })
            else:
                error = f"The bid needs to be larger than the current bid and the starting bid."
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_form": NewBidForm(),
                    "error_message": error,
                    "bids": bids,
                    "bid_submit": False,
                    "comments": comments,
                    "comment_form": AddCommentForm()
                })
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": NewBidForm(),
        "bids": bids,
        "bid_submit": False,
        "comments": comments,
        "comment_form": AddCommentForm()

    })


def watchlist(request):
    user_watchlist = User.objects.get(pk=int(request.user.pk))
    watchlist = user_watchlist.watchlist.all()
    arr = []
    for x in watchlist:
        b = Bid.objects.filter(listing=int(x.pk)).last()
        arr.append(b)

    return render(request, "auctions/watchlist.html", {
        "user_watchlist": watchlist,
        "array": arr
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category_id):
    cat = category_id
    category_name = Category.objects.get(pk=int(cat))
    listings = Auction_Listing.objects.filter(category=int(cat))
    arr = []
    for x in listings:
        b = Bid.objects.filter(listing=int(x.pk)).last()
        arr.append(b)

    return render(request, "auctions/category.html", {
        "cat": cat,
        "cat_name": category_name,
        "listings": listings,
        "array": arr
    })
