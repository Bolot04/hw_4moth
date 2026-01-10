from django import forms

black_list = [
    "phone",
]


class OrderFrom(forms.Form):
    name = forms.CharField(max_length=10, min_length=3)
    description = forms.CharField(max_length=1000)
    price = forms.IntegerField()
    photo = forms.ImageField()