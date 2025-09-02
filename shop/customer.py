from django.db import models

#create your models here.
class Customer(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=20)

   #checking if email is existing or not
    def isexit(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
         
    #to check email id is matching or not
    @staticmethod
    def getemail(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
