from django.db import models


class CustomerTable(models.Model):
    mobNum = models.IntegerField()
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    emailId = models.EmailField(max_length=255,blank=True)
    gender = models.CharField(max_length=10,blank=True)
    dob = models.DateField(blank=True)
    aniversary = models.DateField(blank=True)
    customerNote = models.TextField(blank=True)
    dummy1 = models.IntegerField(blank=True)
    profilePic = models.FileField(upload_to='profilePic/',blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)





