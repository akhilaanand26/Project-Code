from django.shortcuts import render,redirect
from django.contrib import messages
from properties.forms import PropertyForm,PropertyImageForm
from properties.models import Property,PropertyImages,Reservation
from properties.constants import PENDING, CANCELLED, CONFIRMED
from django.shortcuts import get_object_or_404



def properties_views(request):
   properties = Property.objects.filter(owner=request.user).order_by('-created_at')

   return render(request,'owner/properties.html',{'properties':properties})


def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        image_form = PropertyImageForm(request.POST,request.FILES)

        if form.is_valid() and image_form.is_valid():
       
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            img = image_form.save(commit=False)
            img.property_id=obj
            img.save()
            
            messages.success(request, "Property has been added successfully")
            return redirect('owner:properties')
    else:
        form = PropertyForm()
        image_form = PropertyImageForm()
    return render(request,'owner/add_property.html', {'form':form,'image_form':image_form})


def update_property(request, property_id):
    p = get_object_or_404(Property, id=property_id, owner=request.user)
    p_image = PropertyImages.objects.filter(property_id=p.id).first()

    if request.method == "POST":
        form = PropertyForm(request.POST, instance=p)
        image_form = PropertyImageForm(request.POST,request.FILES,instance=p_image)
        
        # do form validation for each field
        if form.is_valid() and image_form.is_valid():
            form.save()
            image_form.save()
            
            messages.success(request, "Property has been updated successfully")
            return redirect('owner:properties')
    else:
        form = PropertyForm(instance=p)
        image_form = PropertyImageForm(instance=p_image)

    return render(request, 'owner/update_property.html', {"form": form,'image_form':image_form})


def delete_property(request, property_id):
    p = get_object_or_404(Property, id=property_id, owner=request.user)
  

    if request.method == "POST":
        p.delete()
       
        messages.success(request, "Property has been deleted successfully")
        return redirect('owner:properties')

    return render(request, 'owner/delete_confirmation.html', {"property": p})

def request_views(request):
   reservations = Reservation.objects.filter(property_id__owner=request.user).order_by('-created_at')

   return render(request,'owner/request.html',{"reservations":reservations})

def accept_request(request, request_id):
    r = get_object_or_404(Reservation, id=request_id, property_id__owner=request.user, status=PENDING)

    if request.method == "POST":
        property = Property.objects.get(id=r.property_id.id)
       
        Reservation.objects.filter(property_id=property.id, status=PENDING).exclude(id=r.id).update(status=CANCELLED)

        r.status = CONFIRMED
        property.is_occupied = True
        r.save()
        property.save()
       
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

def pending_request(request):
       reservations = Reservation.objects.filter(property_id__owner=request.user, status=PENDING).order_by('-created_at')
       
       return render(request, 'owner/request_history.html')