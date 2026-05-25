from django.contrib import admin
from .models import Carousel,Category,Product,UserProfile,Cart,Booking,Feedback

# Register your models here.
admin.site.register(Carousel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(Booking)
admin.site.register(Feedback)