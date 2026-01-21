from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .form import OrderFrom, SearchForm, CommentForm
from .models import Order, Comment

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


def home(request):
    if request.method == "GET":
        return render(request, "base.html")

@login_required(login_url="/login/")
def orders_list(request):
    orders = Order.objects.all()
    if request.method == "GET":
        limit = 3
        forms = SearchForm()
        search = request.GET.get("search")
        category = request.GET.get("category")
        tags = request.GET.getlist("tags")
        ordering = request.GET.get("ordering")
        page = request.GET.get("page") if request.GET.get("page") else 1
        if category:
            orders = orders.filter(category=category)
        if search:
            orders = orders.filter(Q(name__icontains=search) | Q(description__icontains=search)) 
        if tags:
            orders = orders.filter(tag__in=tags)
        if ordering:
            orders = orders.order_by(ordering)
        max_page = range(orders.count() // limit + 1)
        if page:
            orders = orders[limit * (int(page) - 1) : limit * int(page)]
        return render(
            request, "orders/order_list.html", context={"orders": orders, "form": forms, "max_page": max_page[1:]}
        )

@login_required(login_url="/login/")
def orders_detail(request, order_id):
    if request.method == "GET":
        order = Order.objects.filter(id=order_id).first()
        order.views += 1
        order.save()
        forms = CommentForm()
        comments = Comment.objects.filter(order_id=order_id)
        comment_count = comments.count()
        average = sum([Comment.rate for comment in comments]) / comment_count 
        return render(
            request, "orders/order_detail.html", 
            context={
                "order": order,
                "form": forms,
                "comments":comments,
                "average": int(average)
                }
        )
    elif request.method == "POST":
        forms = CommentForm(request.POST)
        if forms.is_valid():
            Comment.objects.create(
                text=forms.cleaned_data["text"],
                order_id=order_id,
                author=request.user,
                rate=forms.cleaned_data["rate"],
            )
            return redirect(f"/orders/{order_id}")

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