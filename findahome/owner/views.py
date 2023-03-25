from django.shortcuts import render,redirect
from django.contrib import messages
from properties.forms import PropertyForm,PropertyImageForm
from properties.models import Property,PropertyImages,Reservation
from properties.constants import PENDING, CANCELLED, ACTIVE,EARLY_OCCUPIED,PAYMENT_PENDING
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from properties.models import MaintenanceRequest
import os
# from .forms import MaintenanceRequestForm
# import googlemaps
# API_KEY = 'AIzaSyAtDBI_DGeh1WZEejPVXosbD1NL1KqLNOo'


def properties_views(request):
   properties = Property.objects.filter(owner=request.user).order_by('-created_at')

   return render(request,'owner/properties.html',{'properties':properties})


def add_property(request):
    ImageFormset = modelformset_factory(PropertyImages, fields=('image',), extra=2)

    if request.method == "POST":
        form = PropertyForm(request.POST,request.FILES)
        #video_form = PropertyForm(request.POST, request.FILES)
        formset = ImageFormset(request.POST, request.FILES, queryset=PropertyImages.objects.none())
        

        # do form validation for each field
        if form.is_valid() and formset.is_valid():
            # add the property via form instance's save() method
            # obj is the Property obj
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            # video = video_form.save(commit=False)
            # video.property_id=obj
            # video.save()

           

            # saving each image
            for f in formset:
                # create an instance of PropertyImages if there is an 'image' present in the form
                # obj is the PropertyImage obj
                if f.cleaned_data.get('image'):
                    image_obj = f.save(commit=False)
                    image_obj.property_id = obj
                    image_obj.save()
            
            messages.success(request, "Property has been added successfully")
            return redirect('owner:properties')
    else:
        form = PropertyForm()
        formset = ImageFormset(queryset=PropertyImages.objects.none())
        # video_form = PropertyImageForm()
      
    return render(request, 'owner/add_property.html', {"form": form, 'formset': formset})

    # if request.method == "POST":
    #     form = PropertyForm(request.POST)
    #     image_form = PropertyImageForm(request.POST,request.FILES)

    #     if form.is_valid() and image_form.is_valid():
       
    #         obj = form.save(commit=False)
    #         obj.owner = request.user
    #         obj.save()

    #         img = image_form.save(commit=False)
    #         img.property_id=obj
    #         img.save()
            
    #         messages.success(request, "Property has been added successfully")
    #         return redirect('owner:properties')
    # else:
    #     form = PropertyForm()
    #     image_form = PropertyImageForm()
    # return render(request,'owner/add_property.html', {'form':form,'image_form':image_form})


def update_property(request, property_id):
    p = get_object_or_404(Property, id=property_id, owner=request.user)
    
    ImageFormset = modelformset_factory(PropertyImages, fields=('image',), extra=2, can_delete=True)
    #ImageFormset = modelformset_factory(PropertyImages, form=PropertyImageForm, fields=('image',), extra=2, can_delete=True)

    if request.method == "POST":
        form = PropertyForm(request.POST,request.FILES,instance=p)
        formset = ImageFormset(request.POST, request.FILES, queryset=PropertyImages.objects.filter(property_id=p.id))
       
  

        # do form validation for each field
        if form.is_valid() and formset.is_valid():   # and video_form.is_valid()
            form.save()



            # if 'delete_video' in request.POST:
            #     if p_video:
            #       os.remove(p_video.video_file.path)
            #       p_video.delete()
            #     image_form.instance.video_file = None
            # elif 'video_file' in request.FILES:
            #     if p_video:
            #       os.remove(p_video.video_file.path)
            #     image_form.save()
            # else:
            #   image_form.save(commit=False)
            #   image_form.video_file = p_video.video_file
            #   image_form.save()
#Check if the video file has changed
            # if 'video_file' in request.FILES:
            #     # Delete the old video file
            #     if p_video:
            #         os.remove(p_video.video_file.path)
            #     # Save the new video file
            #     image_form.save()
            # else:
            #     image_form.save(commit=False)
            #     image_form.video_file = p_video.video_file
            #     image_form.save()
            
        
            # this will give you all forms marked as DELETE
            forms_to_delete = formset.deleted_forms
            for f in formset:
                # create an instance of PropertyImages if there is an 'image' present in the form
                if f.cleaned_data.get('image'):
                        property_image = f.save(commit=False)
                        property_image.property_id = p
                        property_image.save()

                        if f in forms_to_delete:
                            property_image.delete()
            print(form.cleaned_data.get('is_occupied'))
            if not form.cleaned_data.get('is_occupied'):
                reservations=Reservation.objects.filter(property_id=property_id,status=ACTIVE)
                print(reservations)
                if len(reservations)>0:
                    for reservation in reservations:
                        reservation.status=EARLY_OCCUPIED
                        reservation.save()
                
                        
            messages.success(request, "Property has been updated successfully")
            return redirect('owner:properties')
    else:
        form = PropertyForm(instance=p)
        formset = ImageFormset(queryset=PropertyImages.objects.filter(property_id=p.id))
       
    return render(request, 'owner/update_property.html', {"form": form, 'formset': formset})    #,'video_form':video_form

    # p = get_object_or_404(Property, id=property_id, owner=request.user)
    # p_image = PropertyImages.objects.filter(property_id=p.id).first()

    # if request.method == "POST":
    #     form = PropertyForm(request.POST, instance=p)
    #     image_form = PropertyImageForm(request.POST,request.FILES,instance=p_image)
        
        
    #     if form.is_valid() and image_form.is_valid():
    #         form.save()
    #         image_form.save()
            
    #         messages.success(request, "Property has been updated successfully")
    #         return redirect('owner:properties')
    # else:
    #     form = PropertyForm(instance=p)
    #     image_form = PropertyImageForm(instance=p_image)

    # return render(request, 'owner/update_property.html', {"form": form,'image_form':image_form})


def delete_property(request, property_id):
    p = get_object_or_404(Property, id=property_id, owner=request.user)
  

    if request.method == "POST":
        p.delete()
       
        messages.success(request, "Property has been deleted successfully")
        return redirect('owner:properties')

    return render(request, 'owner/delete_confirmation.html', {"property": p})

def request_views(request):
   reservations = Reservation.objects.filter(property_id__owner=request.user, status=PENDING).order_by('-created_at')

   return render(request,'owner/request.html',{"reservations":reservations})

def accept_request(request, request_id):
    r = get_object_or_404(Reservation, id=request_id, property_id__owner=request.user, status=PENDING)

    if request.method == "POST":
        property = Property.objects.get(id=r.property_id.id)
       
        Reservation.objects.filter(property_id=property.id, status=PENDING).exclude(id=r.id).update(status=CANCELLED)

        r.status =PAYMENT_PENDING
        r.save()
        
       
        messages.success(request, "Reservation request for that property has been confirmed successfully")
        return redirect('owner:request')

    return render(request, 'owner/acceptConfirmation.html')



def decline_request(request, request_id):
    r = get_object_or_404(Reservation, id=request_id, property_id__owner=request.user, status=PENDING)

    if request.method == "POST":
        r.status = CANCELLED
        r.save()
        messages.success(request, "Reservation request has been declined successfully")
        return redirect('owner:request')

    return render(request, 'owner/declineConfirmation.html')

def other_request(request):
    
    
    reservations = Reservation.objects.filter(property_id__owner=request.user).exclude(status=PENDING).order_by('-created_at')
       
    return render(request, 'owner/request_history.html',{"reservations":reservations})

# def rental_map(request):
#     gmaps = googlemaps.Client(key=API_KEY)
#     # Do something with the Google Maps client, e.g. retrieve the owner's rental properties
#     return render(request, 'owner/map.html', context)

# def rental_map(request):
#     gmaps = googlemaps.Client(key=API_KEY)
#     properties = get_owner_properties(request.user)
#     markers = []
#     for property in properties:
#         location = gmaps.geocode(property.address)[0]['geometry']['location']
#         markers.append({
#             'lat': location['lat'],
#             'lng': location['lng'],
#             'title': property.name,
#         })
#     context = {
#         'markers': markers,
#     }
#     return render(request, 'owner/map.html', context)

def view_maintenance_requests(request):
    properties = Property.objects.filter(owner=request.user.id)

    maintenance_requests = MaintenanceRequest.objects.filter(property_id__in=properties)
    return render(request, 'owner/view_maintenancerequest.html', {'maintenance_requests': maintenance_requests})






