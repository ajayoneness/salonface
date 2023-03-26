from django.shortcuts import render
from .models import CustomerTable


def cregister(request):

    if request.method=="POST":
        mobno = request.POST['mobnum']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        gender = request.POST['gender']
        dob = request.POST['dob']
        aniversary = request.POST['aniversary']
        note = request.POST['note']
        dummy = request.POST['dummy']
        profileImg = request.FILES['pimg']

        print(mobno,fname,lname,email,gender,dob,aniversary,note,dummy,profileImg)

    return render(request,'Home.html')


def allcustomer(request):
    cusobj = CustomerTable.objects.all()
    return render(request,'allcustomer.html',{"customers":cusobj})


def singleCustomer(request,idd):
    singleObj = CustomerTable.objects.get(id=idd)
    return render(request,'single.html',{'single':singleObj})
