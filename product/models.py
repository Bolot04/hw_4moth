from django.db import models
from django.contrib.auth.models import User
# Create your models here.
"""
create table product (
    id integer primary key,
    name sting 
)
"""


class Category(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    photo = models.ImageField(blank=True, null=True, upload_to="order/")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
        )
    tag = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
    

class Comment(models.Model):
    text = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rate = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"