from django.urls import path
from django.contrib.auth import views as auth_views
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

	path('change-password/', auth_views.PasswordChangeView.as_view()),

	path('reset-password/', auth_views.PasswordResetView.as_view(
		template_name='accounts/reset_password.html'
	), name='password_reset'),
	path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
		template_name='accounts/reset_password_done.html'
	), name='password_reset_done'),
	path('reset-password/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
		template_name='accounts/reset_password_confirm.html'
	), name='password_reset_confirm'),
	path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
		template_name='accounts/reset_password_complete.html'
	), name='password_reset_complete'),
]