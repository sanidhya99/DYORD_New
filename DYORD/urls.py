"""
URL configuration for DYORD project.

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
from django.contrib import admin
from django.urls import path,include
from register import urls as a
from dfy import urls as y
# from dfo import urls as o
# from dfg import urls as g
# from result import urls as r

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(a)),
    path('designforyou/', include(y)),
]
