"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .views import UserProfileView, TransactionListView, CoinTransferView, CoinBurnView

urlpatterns = [
    path('api/users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('api/coins/transfer/', CoinTransferView.as_view(), name='coin-transfer'),
    path('api/coins/burn/', CoinBurnView.as_view(), name='coin-burn'),
]
# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... ваши существующие URL-пути
]
