from django.shortcuts import render,redirect
from .models import * 
from django.http import JsonResponse
import json 
from django.contrib import messages
import datetime 
# Create your views here.
def store(request):
	if request.user.is_authenticated:
		# customer = request.user#one to one relationship between User and Customer
		if Customer.objects.filter(user=request.user).exists():
			customer = Customer.objects.get(user=request.user)
		else:
			customer = Customer.objects.create(user=request.user,email = request.user.email,name = request.user.first_name)
			print(customer)
			customer.save()
		
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartitems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartitems = order['get_cart_items']

	prdt = Product.objects.all();
	return render(request,'store.html',{'product':prdt,'cartitems':cartitems})

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer#one to one relationship between User and Customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartitems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartitems = order['get_cart_items']
		messages.info(request,'you are not logged in')
		return render(request,'login.html')

	context = {'items':items,'order':order,'cartitems':cartitems}
	return render(request,'cart.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer#one to one relationship between User and Customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartitems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartitems = order['get_cart_items']
		messages.info(request,'you are not logged in')
		return render(request,'login.html')

	context = {'items':items,'order':order,'cartitems':cartitems}
	return render(request,'checkout.html',context) 

def add(request): 
	if request.user.is_authenticated: 
		if request.method=='POST':
			productid = request.POST.get('try')#fetching the value whose name is try
			# print(productid)
			product = Product.objects.get(id = productid)
			# prdt = OrderItem.objects.create(product = product)
			# prdt.save();
			customer = request.user.customer
			if Order.objects.filter(customer=customer, complete=False).exists():
				order = Order.objects.get(customer=customer, complete=False)

			else:
				order = Order.objects.create(customer=customer, complete=False)
				print(order)
				order.save()

			if OrderItem.objects.filter(order=order,product=product).exists():
				orderitem = OrderItem.objects.get(order=order,product=product)
				orderitem.quantity = (orderitem.quantity + 1)
				orderitem.save()

			else:
				orderitem = OrderItem.objects.create(order=order, product=product,quantity=1)
				orderitem.save()
			return redirect('store')
	else:
		return redirect('login')

def add1(request): 
	if request.user.is_authenticated: 
		if request.method=='POST':
			productid = request.POST.get('try')#fetching the value whose name is try
			# print(productid)
			product = Product.objects.get(id = productid)
			# prdt = OrderItem.objects.create(product = product)
			# prdt.save();
			customer = request.user.customer
			if Order.objects.filter(customer=customer, complete=False).exists():
				order = Order.objects.get(customer=customer, complete=False)

			else:
				order = Order.objects.create(customer=customer, complete=False)
				print(order)
				order.save()

			if OrderItem.objects.filter(order=order,product=product).exists():
				orderitem = OrderItem.objects.get(order=order,product=product)
				orderitem.quantity = (orderitem.quantity + 1)
				orderitem.save()

			else:
				orderitem = OrderItem.objects.create(order=order, product=product,quantity=1)
				orderitem.save()
			return redirect('cart')

def remove(request):
	if request.user.is_authenticated: 
		if request.method=='POST':
			productid = request.POST.get('try')#fetching the value whose name is try
			# print(productid)
			product = Product.objects.get(id = productid)
			# prdt = OrderItem.objects.create(product = product)
			# prdt.save();
			customer = request.user.customer
			if Order.objects.filter(customer=customer, complete=False).exists():
				order = Order.objects.get(customer=customer, complete=False)

			else:
				order = Order.objects.create(customer=customer, complete=False)
				print(order)
				order.save()

			if OrderItem.objects.filter(order=order,product=product).exists():
				orderitem = OrderItem.objects.get(order=order,product=product)
				orderitem.quantity = (orderitem.quantity - 1)
				orderitem.save()
			if orderitem.quantity <= 0:
				orderitem.delete()
			return redirect('cart')

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		total = int(data['shipping']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		newaddress = ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
		newaddress.save()
	return JsonResponse('Payment submitted..', safe=False)

def filters(request):
	title = request.POST.get('type')
	if request.user.is_authenticated:
		if Customer.objects.filter(user=request.user).exists():
			customer = Customer.objects.get(user=request.user)
		else:
			customer = Customer.objects.create(user=request.user,email = request.user.email,name = request.user.first_name)
			print(customer)
			customer.save()
		
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartitems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
		cartitems = order['get_cart_items']

	prdt = Product.objects.filter(title=title)
	return render(request,'store.html',{'product':prdt,'cartitems':cartitems})
	
