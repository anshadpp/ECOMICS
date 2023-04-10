from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views import View
from . models import Product, Customer, Cart ,OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import  messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@login_required
def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request,"app/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())


@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())
    def post(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, "app/customerregistration.html", locals())


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            pincode = form.cleaned_data['pincode']

            reg= Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,pincode=pincode)
            reg.save()
            messages.success(request,"Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())
@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())


@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.pincode = form.cleaned_data['pincode']
            add.save()
            messages.success(request, "Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

@login_required
def add_to_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        amount = amount + p.product.discounted_price
    totalamount=amount
    return render(request, 'app/addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            famount=famount+p.product.discounted_price
        totalamount = famount
        return render(request, 'app/checkout.html', locals())
@login_required
def orderplaced(request):

    user = request.user
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, product=c.product).save()
        c.delete()

    return redirect("orders")
@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())
@login_required
def search(request):
    query=request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())



def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            amount=amount+p.product.discounted_price
        totalamount = amount
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

