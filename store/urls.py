from django.urls import path
from . import views

urlpatterns = [ 
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('add/',views.add,name="add"),
	path('add1/',views.add1,name="add1"),
	path('remove/',views.remove,name="remove"),
	path('process_order/',views.processOrder,name="process_order"),
	path('filters/',views.filters,name="filters"),
]