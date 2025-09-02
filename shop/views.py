from django.shortcuts import render
from django.http import HttpResponse
from .product import product
from .category import Category
from django.contrib.auth.hashers import check_password
from .customer import Customer
from django.shortcuts import render, redirect
from .cart import Cart






# Create your views here.
def home(request):
    products=product.objects.all()
    categories=Category.objects.all()
    categoryID=request.GET.get('category')
    if categoryID:
        products=product.get_category_id(categoryID)
    else:
        products=product.objects.all()
    data={'products':products,'categories':categories}
    return render(request,'index.html',data)

#signup form
def signup(request):
    if request.method=="GET":
        return render(request,"signup.html")
    else:
        fn=request.POST['fn']
        ln=request.POST['ln']
        email=request.POST['email']
        mobile=request.POST['mobile']
        password=request.POST['password']
        
        
        userdata=[fn,ln,email,mobile,password]
        print(userdata)
        uservalues={
            'fn':fn,
            'ln':ln,
            'email':email,
            'mobile':mobile
            
        }

        #storing object
        customerdata=Customer(first_name=fn,last_name=ln,email=email,mobile=mobile,password=password)
        #validation
        error_msg=None
        success_msg=None
        if(not fn):
            error_msg="First name should not be empty"
        elif(not ln):
            error_msg="last name should not be empty"
        elif(not email):
            error_msg="email field should not  be empty"
        elif(not mobile):
            error_msg="Mobile field should not be empty"
        elif(not password):
            error_msg="password should not be empty"
        elif(customerdata.isexit()):
            error_msg="Email Already Exists"
        if(not error_msg):
            success_msg="Account Created successfully"
            customerdata.save()
            msg={'success':success_msg}
            return render(request,'signup.html',msg)
        else:
            msg={'error':error_msg,'value':uservalues}
            return render(request,'signup.html',msg)
        
#login page
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        email=request.POST['email']
        password=request.POST['password']

        #to check email found or not
        users=Customer.getemail(email)
        error_msg=None
        if users:
            #if email found check password
            check=check_password(password,users.password)
            #if password found
            if check:
                return redirect('/')
            else:
                error_msg="password is incorrect"
                msg={'error':error_msg}
                return render(request,'login.html',msg)
        else:
            error_msg="email is in correct"
            msg={'error':error_msg}
            return render(request,'login.html',msg)



#logout page
def logout(request):
    if request.method=='GET':
         return redirect('login')
       

#cart page
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('/')

def view_cart(request):
    cart = Cart(request)
    cart_items = []
    total_price = 0
    for pid, qty in cart.get_cart_items().items():
        try:
            prod = product.objects.get(id=pid)
            prod.quantity = qty
            prod.total = prod.price * qty
            total_price += prod.total
            cart_items.append(prod)
        except product.DoesNotExist:
            continue
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('/cart')


#buy now
def buy_now(request, product_id):
    cart = Cart(request)
    pid = str(product_id)
    quantity = cart.cart.get(pid, 0)
    try:
        prod = product.objects.get(id=pid)
        total = prod.price * quantity
        return render(request, 'buy_now.html', {
            'product': prod,
            'quantity': quantity,
            'total': total
        })
    except product.DoesNotExist:
        return redirect('view_cart')


def increase_quantity(request, product_id):
    cart = Cart(request)
    pid = str(product_id)
    if pid in cart.cart:
        cart.cart[pid] += 1
    cart.save()
    return redirect('view_cart')


def decrease_quantity(request, product_id):
    cart = Cart(request)
    pid = str(product_id)
    if pid in cart.cart and cart.cart[pid] > 1:
        cart.cart[pid] -= 1
    cart.save()
    return redirect('view_cart')





