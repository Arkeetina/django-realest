from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing

def index(req):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 3)
    page = req.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }
    return render(req, 'listings/listings.html', context)

def listing(req, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    context = {
        'listing': listing
    }
    return render(req, 'listings/listing.html', context)

def search(req):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in req.GET:
        keywords = req.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # City
    if 'city' in req.GET:
        city = req.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    # State
    if 'state' in req.GET:
        state = req.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in req.GET:
        bedrooms = req.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    
    # Price
    if 'price' in req.GET:
        price = req.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'price_choices': price_choices,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'listings': queryset_list,
        'values': req.GET
    }
    return render(req, 'listings/search.html', context)