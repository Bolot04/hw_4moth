from django.contrib import admin

from product.models import Category, Order

# Register your models here.
admin.site.register(Order)
admin.site.register(Category)