from . import views
from django.urls import path

urlpatterns = [
    path('',views.cregister,name="cregister"),
    path('allcustomer/',views.allcustomer,name="allcustomer"),
    path('single/<int:idd>',views.singleCustomer,name="single"),
]
