from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import listingform, BidForm

from .models import User, listing, bids, comments


def index(request):
    listings = listing.objects.exclude(isactive=False)
    message = None  # Initialize the message as None

    if request.user.is_authenticated:
        won_bids = bids.objects.filter(owner=request.user, title__isactive=False).order_by('-bid_price')
        if won_bids.exists():
            won_listing = won_bids.first().title
            won_price = won_bids.first().bid_price
            # Check if the user is not the creator of the listing
            if won_listing.creator != request.user:
                message = f"Congratulations! You've won the {won_listing} for ${won_price}"

    return render(request, "auctions/index.html", {
        "listings": listings,
        "message": message,
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

@login_required
def create(request):
    if request.method == 'POST':
        form = listingform(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.creator = request.user
            new_listing.save()

            return HttpResponseRedirect(reverse('index'))
    else :
        form = listingform
   
    return render(request, 'auctions/create.html', {"form": form})

@login_required
def watchlist(request, listing_id):
    user = request.user
    listing_obj = listing.objects.get(id=listing_id)
    if listing_obj in user.watchlist.all():
        user.watchlist.remove(listing_obj)
    else:
        user.watchlist.add(listing_obj)
    return HttpResponseRedirect(reverse('items', args=[listing_id]))

@login_required
def showlists(request):
    user = request.user
    watchlists = user.watchlist.all()
    listings = listing.objects.all()
    return render(request, "auctions/watchlist.html", {
        "watchlists" : watchlists,
        "listing" : listings
    })

@login_required
def items(request, listing_id):
    item = listing.objects.get(id=listing_id)
    cmnts = comments.objects.all()

    if request.method == 'POST':


        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            bid_price = bid_form.cleaned_data['bid_price']

            if bid_price > item.price:
                item.price = bid_price
                item.save()

                new_bid = bid_form.save(commit=False)
                new_bid.owner = request.user
                new_bid.title = item
                new_bid.save()

                return render(request, "auctions/item.html", {
                    "item": item,
                    "message":"you have been bidded successfully!",
                    "bid_form":bid_form,
                    "al": "success",
                    "comments": cmnts
                })
            else:
                return render(request, "auctions/item.html", {
                    "item" : item,
                    "message" : "the bid should be greater than the price!",
                    "bid_form": bid_form,
                    "al": "danger",
                    "comments": cmnts
                })
    else:
        bid_form = BidForm()

    return render(request, "auctions/item.html", {
        "item": item,
        "bid_form":bid_form,
        "comments": cmnts
    })

@login_required
def add_comment(request, item_id):
    if request.method == 'POST':
        # Get the comment text from the form data
        comment_text = request.POST.get('comment')

        # Get the item for which the comment is being added
        id_item = listing.objects.get(pk=item_id)

        # Create a new comment and save it
        comment = comments(content=comment_text, customer=request.user, item_id=id_item)
        comment.save()

    # Redirect back to the item's detail page
    return HttpResponseRedirect(reverse('items', args=[item_id]))


@login_required
def endbid(request, item_id):
    if request.method == 'POST':
        endtask = request.POST.get('endtask')

        id_item = listing.objects.get(pk=item_id)

        id_item.isactive = False
        id_item.save()


    return HttpResponseRedirect(reverse('index'))