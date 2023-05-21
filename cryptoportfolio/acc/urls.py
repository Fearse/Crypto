"""
URL configuration for cryptoportfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('',views.acc_home,name='home'),
    path('create',views.acc_create,name='create'),
    path('support', views.support, name='support'),
    path('<int:pk>',views.portfolio,name='portfolio'),
    path('<int:pk>/transaction',views.transaction,name='transaction'),
    path('<int:pk>/change',views.change,name='change'),
    path('<int:pk>/delete',views.delete,name='delete'),
    path('exit/', authViews.LogoutView.as_view(next_page='/login/check'), name='exit'),
]
