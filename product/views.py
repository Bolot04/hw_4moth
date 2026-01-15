from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .form import OrderFrom
from .models import Order

# Create your views here.

"""
select * form product;
"""
# product = """
#     select * from product where name = '{user_input}';
# """
"""
select * from product ILIKE where = "%phone%"
"""

"""
insert into product (name, description, price) values ('name', 'description', 100);
"""

# GET - для просмотра данных
# POST - для отправки данных
# PUT - для обновления данных
# PATCH - для обновления частичных данных
# DELETE - для удаления

@login_required(login_url="/login/")
def home(request):
    if request.method == "GET":
        return render(request, "base.html")

@login_required(login_url="/login/")
def orders_list(request):
    if request.method == "GET":
        orders = Order.objects.all()
        return render(
            request, "orders/order_list.html", context={"orders": orders}
        )

@login_required(login_url="/login/")
def orders_detail(request, order_id):
    if request.method == "GET":
        order = Order.objects.filter(id=order_id).first()
        return render(
            request, "orders/orders_detail.html", context={"order": order}
        )

@login_required(login_url="/login/")
def order_create_view(request):
    if request.method == "GET":
        form = OrderFrom()
        return render(request, "orders/order_create.html", context={"form": form})
    elif request.method == "POST":
        form = OrderFrom(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            Order.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                photo=form.cleaned_data["photo"],
            )
        return HttpResponse("Order created")   