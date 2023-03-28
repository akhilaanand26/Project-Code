from django.contrib import admin
from .models import District, Property, PropertyImages,Wishlist,Comment

# Register your models here.

class PropertyImagesInline(admin.StackedInline):
    model = PropertyImages

class PropertyAdmin(admin.ModelAdmin):
    model = Property
    inlines = [PropertyImagesInline,]

    list_display = ('title', 'plot_area', 'rate', 'zip_code', 'owner', 'is_occupied')

    fieldsets = (
        (None, { 'fields': ('title', 'description', 'owner', 'is_occupied', ) }),
        ('Address', { 'fields': ('address_1', 'city', 'district', 'zip_code','location',) }),
        ('Other Info', { 'fields': ('no_of_floors',   'plot_area', 'rate', 'has_watersupply', 'has_electricity',
        'no_of_bathrooms_inside','no_of_bathrooms_outside','no_of_bedrooms','master_bedroon','no_of_livingrooms','kitchen','dining_hall','feature_1','feature_2',) }),
        #('Property Images',{ 'fields': ('Image',)}),
    )

    search_fields = ('title', 'zip_code', 'city','district', 'description')

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImages)
admin.site.register(District)
admin.site.register(Comment)
admin.site.register(Wishlist)

