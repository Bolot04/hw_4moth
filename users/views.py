from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/login/")
def register_view(request):
    if request.method == "GET":
        forms = RegisterForm()
        return render(request, "users/register.html", context={"form": forms})
    elif request.method == "POST":
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.cleaned_data.__delitem__("confirm_password")
            User.objects.create_user(
                **forms.cleaned_data
            )
            return HttpResponse("User Created")
        return HttpResponse("Invalid from")


@login_required(login_url="/login/")
def login_view(request):
    if request.method == "GET":
        forms = LoginForm
        return render(request, "users/login.html", context={"form": forms})
    elif request.method == "POST":
        forms = LoginForm(request.POST)
        if forms.is_valid():
            user = authenticate(
                **forms.cleaned_data
                )
            login(request, user)
            return HttpResponse("User logged in")


@login_required(login_url="/login/")     
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return HttpResponse("User logged out")