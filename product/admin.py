from django.contrib import admin

from product.models import Category, Order, Tag, Comment

# Register your models here.
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)