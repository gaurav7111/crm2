from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm    
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user,allowed_users,admin_only

from django.contrib import messages

# Create your views here.
@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'app/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
                messages.info(request,'Username OR password is incorrect')  
             
    context = {}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    deliverd = orders.filter(status='Deliverd').count()
    pending = orders.filter(status='Pending').count()


    context = {'orders': orders, 'customers': customers,'total_orders': total_orders,'deliverd': deliverd, 'pending': pending}
    return render(request,'app/dashbord.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders =request.user.customer.order_set.all()
    total_orders = orders.count()
    deliverd = orders.filter(status='Deliverd').count()
    pending = orders.filter(status='Pending').count()


    context={'orders':orders,'total_orders': total_orders,'deliverd': deliverd, 'pending': pending}
    return render(request,'app/user.html',context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance= customer)

    if request.method == 'POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request,'app/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'app/product.html',{"products": products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)    
    orders = customer.order_set.all()
    myFilter =OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs
    order_count = orders.count()
    context ={'customer': customer,'orders': orders,'order_count': order_count,'myFilter': myFilter}
    return render(request,'app/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request,'app/order_form.html',context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order =Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form} 
    return render(request,'app/order_form.html',context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order =Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {'item': order}
    return render(request,'app/delete.html',context)
