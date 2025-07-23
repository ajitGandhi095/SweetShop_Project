"""
URL configuration for EcommerceProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from EApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_view, name='home'),
    path('wedding-shop/', views.wedding_view),
    path('about/', views.about_view),
    path('contact/', views.contact_view),
    path('shop/', views.shop_view),
    path('signup/', views.signup_view),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view),
    path('homepage/', views.home_view, name="homepage"),
    path('home-about/', views.home_about_view),
    path('home-contact/', views.home_contact_view),
    path('home-shop/', views.home_shop_view),
    path('cart/', views.view_cart, name="view_cart_item"),
    path('add/<int:id>', views.add_to_cart_view, name="add_to_cart"),
    path('remove/<int:id>', views.remove_from_cart, name="remove_cart"),
    path('user-profile/', views.useraccount_view),
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-dashboard/', views.admin_dashboard_view, name="admin-dashboard"), 
    path('update/<int:id>', views.product_update_view),
    path('delete/<int:id>', views.product_delete_view),
    path('delete-user/<int:id>', views.user_delete_view),
    path('checkout/', views.checkout_view), 
    path('payment/', views.paymentpage_view, name="payment_page"),
    path('payment-success/', views.paymentsuccess_view, name="payment_success")
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
