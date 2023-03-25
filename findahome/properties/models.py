from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone
from django.urls import reverse
from users.models import User
from .constants import PENDING, CANCELLED, EARLY_OCCUPIED,ACTIVE,PAYMENT_PENDING
from django.core.validators import FileExtensionValidator
#from location_field.models.plain import PlainLocationField


class District(models.Model):
    name = models.CharField(max_length=50,unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'district'
        verbose_name_plural = 'districts'

    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=230)
    description = models.TextField()
    no_of_floors = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])
    
    no_of_bathrooms_inside= models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])
    no_of_bathrooms_outside= models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(12)])
    no_of_bedrooms = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])
    master_bedroon = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])
    
    no_of_livingrooms = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])
    dining_hall = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])
    kitchen = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(12)])


    feature_1 = models.CharField( max_length=100)
    feature_2 = models.CharField( max_length=100)

    plot_area = models.PositiveIntegerField(validators=[MinValueValidator(500)]) # sqft
    
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    has_watersupply = models.BooleanField(default=True)
    has_electricity = models.BooleanField(default=True)

    address_1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    zip_code = models.CharField(max_length=6, validators=[RegexValidator(regex='^[0-9]{6}$', message='Invalid Zip Code')])
    video_file = models.FileField(upload_to='properties/',validators=[FileExtensionValidator(['mp4', 'avi'])])
    

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # location = PlainLocationField(based_fields=['city'], zoom=7)

    is_occupied = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now) # can be edited/updated manually
    updated_at = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('properties:detail', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'property'
        verbose_name_plural = 'properties'

class PropertyImages(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/')


    def __str__(self):
        return self.property_id.title
    
    # class Meta:
    #     verbose_name = 'propertyimage'
    #     verbose_name_plural = 'Property Images'

class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now) # can be edited/updated manually
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'{self.user_id.first_name} - {self.property_id.title}'

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'wishlist'
        verbose_name_plural = 'wishlists'

class Reservation(models.Model):
    ALL_STATUSES = [
        (PENDING, "Pending"),
        (CANCELLED, "Cancelled"),
        (EARLY_OCCUPIED,"Early Occupied"),
        (ACTIVE,"Active"),
        (PAYMENT_PENDING,"Payment Pending"),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ALL_STATUSES, default=PENDING)

    created_at = models.DateTimeField(default=timezone.now) # can be edited/updated manually
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property_id.title + " - " + self.user_id.first_name

    

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    comment=models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        return self.comment


class MaintenanceRequest(models.Model):
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description


# class Lease(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.user_id} - {self.property_id}"




    
    



