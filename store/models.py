from django.db import models
from django.contrib.auth.models import User
# Create your models here.\

class Customer(models.Model): 
	user = models.OneToOneField(User,on_delete = models.CASCADE,null=True,blank=True)
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.IntegerField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	title = models.CharField(max_length=100,null=True)

	def __str__(self):
		return self.name 

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital==False:
				shipping = True
		return False
	

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		sum=0
		for item in orderitems:
			sum = sum + item.get_total
		return sum

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		sum=0
		for item in orderitems:
			sum = sum + item.quantity
		return sum

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField()
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
