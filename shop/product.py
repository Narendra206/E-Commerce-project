from django.db import models
from .category import Category
# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=30)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='img')
    desc=models.TextField()
    price=models.IntegerField()



    #static method
    @staticmethod
    def get_category_id(get_id):
      if get_id:
         return product.objects.filter(category=get_id)
      else:
         return product.objects.all()  

