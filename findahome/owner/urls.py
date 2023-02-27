from django.urls import path
from .views import properties_views,add_property, delete_property, update_property,request_views,accept_request,decline_request,pending_request

app_name='owner'

urlpatterns = [
    path('',properties_views,name='properties'),
    path('add_property/',add_property,name='add_property'),
    path('delete_property/<int:property_id>/',delete_property,name='delete_property'),
    path('update_property/<int:property_id>/',update_property,name='update_property'),
    path('request/',request_views,name='request'),
    path('pending_request/',pending_request, name='pending_request'),
    path('accept-request/<int:request_id>/',accept_request, name='accept_request'),
    path('decline-request/<int:request_id>/',decline_request, name='decline_request'),
]
