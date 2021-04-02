from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('detail/<int:id>/', views.detail, name="detail"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('login/', views.signIn, name="login"),
	path('logout/', views.signOut, name="logout"),
	path('register/', views.register, name="register"),
]