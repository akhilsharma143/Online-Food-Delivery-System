from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(FoodItem)
admin.site.register(Cart)
admin.site.register(LikedItem)
admin.site.register(UserSignup)
admin.site.register(Address)
admin.site.register(Order)