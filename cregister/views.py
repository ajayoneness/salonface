from django.shortcuts import render
from .models import CustomerTable
import base64
from django.core.files.base import ContentFile

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
        dummy = 1
        try:
            profileImg = request.FILES['pimg']
        except:
            captured_image_data = request.POST['captured_image_data']
            format, imgstr = captured_image_data.split(';base64,')
            ext = format.split('/')[-1]
            profileImg = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


        print(profileImg)

        print(mobno,fname,lname,email,gender,dob,aniversary,note,dummy,profileImg)
        cusTbl = CustomerTable(mobNum=mobno,fname=fname, lname=lname, emailId=email,gender=gender,dob=dob,aniversary=aniversary, customerNote=note,dummy1=dummy, profilePic=profileImg)
        cusTbl.save()


    return render(request,'Home.html')


def allcustomer(request):
    if request.method=="POST":
        searchoption = request.POST['search']
        searchbox = request.POST['searchbox']

        if searchoption == 'note':
            cusobj=CustomerTable.objects.filter(customerNote__icontains=searchbox)

        if searchoption == "name":
            cusobj = CustomerTable.objects.filter(fname__icontains=searchbox)
        if searchoption == "number":
            cusobj = CustomerTable.objects.filter(mobNum__icontains=searchbox)

        return render(request, 'allcustomer.html', {"customers": cusobj})



    cusobj = CustomerTable.objects.all()
    return render(request,'allcustomer.html',{"customers":cusobj})


def singleCustomer(request,idd):
    singleObj = CustomerTable.objects.get(id=idd)
    return render(request,'single.html',{'single':singleObj})
