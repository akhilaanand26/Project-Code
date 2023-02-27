from django.shortcuts import render,redirect
from django.contrib import messages
from properties.models import Property
from .models import Wishlist
from .models import Reservation
from .models import Comment
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.
def home(request):
    latest_properties = Property.objects.all().filter(is_occupied=False).order_by('-created_at')
    if request.user.is_authenticated:
        for p in latest_properties:
            p.has_wishlisted = p.wishlist_set.filter(user_id=request.user).count() > 0
            
    return render(request,'properties/home.html',{'latest_properties':latest_properties})
    

def reservation(request):
    
    return render(request,'properties/reservation.html')

def search(request):
    query = request.GET.get('q')

    if not query:
        return redirect('properties:home')

   
    min_price = 1000
    max_price = 50000
    min_no_of_floors = 1
    max_no_of_floors = 12
    min_no_of_bedrooms = 1
    max_no_of_bedrooms = 12
    min_no_of_sqft = 1
    max_no_of_sqft = 50000

    current_min_price = request.GET.get('min-price')
    current_max_price = request.GET.get('max-price')
    current_min_sqft = request.GET.get('min-sqft')
    current_max_sqft = request.GET.get('max-sqft')
    current_no_of_bedrooms = request.GET.get('bedrooms')
    current_no_of_floors = request.GET.get('floors')


    # make query to db
    # search q in title, city, district, address_1, zip_code
    properties = Property.objects.filter(Q(title__icontains=query) | Q(city__icontains=query) | Q(district__name__icontains=query) | Q(address_1__icontains=query) | Q(zip_code__icontains=query)).exclude(is_occupied=True)
    print(properties)
    if current_min_price:
        properties = properties.filter(rate__gte = current_min_price)

    if current_max_price:
        properties = properties.filter(rate__lte = current_max_price)

    if current_min_sqft:
        properties = properties.filter(plot_area__gte = current_min_sqft)

    if current_max_sqft:
        properties = properties.filter(plot_area__lte = current_max_sqft)

    if current_no_of_floors:
        properties = properties.filter(no_of_floors = current_no_of_floors)

   
    
    properties = properties.order_by('-created_at')
  
    

   
    return render(request, 'properties/search.html', 
        { "q": query, 
            "min_price": min_price or "", 
            "max_price": max_price or "", 
            "min_no_of_floors": min_no_of_floors or "", 
            "max_no_of_floors": max_no_of_floors or "", 
            "min_no_of_bedrooms": min_no_of_bedrooms or "", 
            "max_no_of_bedrooms": max_no_of_bedrooms or "", 
          
            "min_no_of_sqft": min_no_of_sqft  or "", 
            "max_no_of_sqft": max_no_of_sqft or "", 

            "current_no_of_bedrooms": current_no_of_bedrooms  or "",
            "current_no_of_floors": current_no_of_floors  or "",
           
            "current_min_price": current_min_price  or "",
            "current_max_price": current_max_price  or "",
            "current_min_sqft": current_min_sqft  or "",
            "current_max_sqft": current_max_sqft  or "",

            "properties": properties
        })



def property_details(request,propertydetails_id):
    details = Property.objects.get(id=propertydetails_id)
    if request.user.is_authenticated:
        has_wishlisted = Wishlist.objects.filter(user_id=request.user, property_id=propertydetails_id).exists()
    else:
        has_wishlisted = False
         
   
    return render(request,'properties/property_details.html',{"property": details, "has_wishlisted": has_wishlisted})

def property_reserve(request):
    id = request.POST.get('id')

    property = get_object_or_404(Property, id=id)

    
    reservation = Reservation(user_id=request.user, property_id=property)
    reservation.save()
    messages.info(request, "Your Reservation request has been sent successfully! ")
    return redirect('properties:property_details', propertydetails_id=id)


def wishlist(request):
    wishlist_properties = Wishlist.objects.filter(user_id=request.user)
    return render(request,'properties/wishlist.html',{"wishlist_properties":wishlist_properties})
   

    
def add_or_remove_wishlist(request,propertydetails_id):
    
    wishlisted = None
    print(propertydetails_id)
    if request.method == "POST":
        

        property = get_object_or_404(Property, id=propertydetails_id)

        # create a wishlist if not exists, else remove it if exists
        wishlist = Wishlist.objects.filter(user_id=request.user, property_id=property)
        
        if len(wishlist) > 0:
            # remove it
            wishlist[0].delete()
            wishlisted = False
        else:
            Wishlist.objects.create(user_id=request.user, property_id=property)
            wishlisted = True
    return JsonResponse({ 'wishlisted': wishlisted })


def add_comment(request, id):
    
    

 return redirect('properties:properties_details', id=id)




