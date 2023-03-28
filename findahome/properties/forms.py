from django import forms

from .models import Property,PropertyImages
from .models import MaintenanceRequest

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('title', 'description', 'no_of_floors', 'no_of_bathrooms_inside','no_of_bathrooms_outside','no_of_bedrooms','master_bedroon','no_of_livingrooms','kitchen','dining_hall','kitchen','feature_1','feature_2','plot_area','rate','has_electricity','has_watersupply','address_1','city','district','zip_code','is_occupied','video_file','location')
     
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImages
        fields = ('image',)   
       

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['description']



       
