from django.urls import path
from .views import home
from .views import wishlist
from .views import search
from .views import reservation
from .views import property_details
from .views import add_comment
from .views import payment
from .views import thanks
from .views import terms
from .views import property_reserve,add_or_remove_wishlist
from .views import  create_maintenance_request,show_video
app_name='properties'

urlpatterns = [
    path('',home,name='home'),
    path('search/', search, name='search'),
    path('wishlist/',wishlist,name='wishlist'),
    path('reservation/',reservation,name='reservations'),
    path('property_details/<int:propertydetails_id>/',property_details,name='property_details'),
    path('property/reserve',property_reserve,name='property_reserve'),
    path('wishlists/property/<int:propertydetails_id>/',add_or_remove_wishlist, name='add_or_remove_wishlist'),
    path('property/<int:id>/add-comment', add_comment, name='add_comment'),
    path('payment/<int:property_id>/',payment,name='payment'),
    path('terms/<int:property_id>/',terms,name='terms'),
    path('maintenance_request/<int:property_id>/', create_maintenance_request,name='maintenancerequest'),
    #path('property/<int:property_id>/show_video/', show_video, name='show_video'),
    #path('show_video/<int:property_id>/', show_video, name='show_video'),
    path('show_video/<int:property_id>/', show_video, name='show_video'),
]