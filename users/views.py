from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from users.models import Profile
# Create your views here.



def register_view(request):
    if request.method == "GET":
        forms = RegisterForm()
        return render(request, "users/register.html", context={"form": forms})
    elif request.method == "POST":
        forms = RegisterForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.cleaned_data.__delitem__("confirm_password")
            age = forms.cleaned_data.pop("age")
            photo = forms.cleaned_data.pop("photo")
            user = User.objects.create_user(
                **forms.cleaned_data
            )
            if user:
                Profile.objects.create(user=user, age=age, photo=photo)
            return redirect("/login/")
        return HttpResponse("Invalid from")



def login_view(request):
    if request.method == "GET":
        forms = LoginForm()
        return render(request, "users/login.html", context={"form": forms})
    elif request.method == "POST":
        forms = LoginForm(request.POST)
        if forms.is_valid():
            user = authenticate(
                username=forms.cleaned_data["username"],
                password=forms.cleaned_data["password"]
           )
            login(request, user)
            return redirect("/")


@login_required(login_url="/login/")     
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")
    

def profile_view(request):
    if request.method == "GET":
        user = request.user
        return render(request, "users/profile.html")