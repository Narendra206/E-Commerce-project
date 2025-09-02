from django.contrib import admin
from .product import product
from .category import Category
from.customer import Customer

# Register your models here.
class Categoryinfo(admin.ModelAdmin):
    list_display=["name"]

class productinfo(admin.ModelAdmin):
    list_display=["name","category","price"]  

class Customerinfo(admin.ModelAdmin):
    list_display=["first_name","last_name","email"]      
  
admin.site.register(product,productinfo)
admin.site.register(Category,Categoryinfo)
admin.site.register(Customer,Customerinfo)  