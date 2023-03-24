from django.shortcuts import render
from .models import CustomerTable


def cregister(request):
    return render(request,'Home.html')


def allcustomer(request):
    cusobj = CustomerTable.objects.all()
    return render(request,'allcustomer.html',{"customers":cusobj})
