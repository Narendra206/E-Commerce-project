from django.db import models

#create your models here
class Category(models.Model):
    name=models.CharField(max_length=20) 


    def __str__(self):
        return self.name