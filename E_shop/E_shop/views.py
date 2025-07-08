from django.shortcuts import render ,redirect,HttpResponse
from app.models import Category,Product,Contact,Order, Brand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from app.models import UserCreateForm

from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def Master(request):
    return render(request, "master.html")


def Index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    product = Product.objects.all()

    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(subcategory=categoryID)
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()

    context = { "categorys" : category ,
                "products" : product ,
                "brand" : brand ,
                }

    return render(request, "index.html", context)


def Signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            login(request, new_user)
            print(new_user)
            return redirect('index')

    else:
        form = UserCreateForm()

    context = { 'form' : form, }
    return render(request, 'registration/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')




#Add to cart
@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def Contact_Page(request):
    if request.method == "POST":
        contact = Contact(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message')
        )
        contact.save()
    return render(request, "contact.html")


def Checkout_page(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode  = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        print(cart)

        for i in cart:
            a = int(cart[i]['price'])
            b = cart[i]['quantity']
            total = a * b

            order = Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                total = total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')
    return HttpResponse('this is a check out')


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    #order = Order.objects.all() #for all orders present in database it displays
    order = Order.objects.filter(user = user)   #it filters/displays only particular orders of user
    context = {
        'order' : order,
    }
    print(user,order)
    return render(request, 'order.html',context)



def Product_Page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    product = Product.objects.all()

    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(subcategory=categoryID)
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()
    context = {
        "category" : category,
        "brand" : brand,
         "products" : product,
    }
    return render(request, 'product.html', context)



def Product_Details(request,id):
    product = Product.objects.filter(id=id).first()
    context = {
        "product" :product ,
    }
    return render(request, 'product_details.html', context )


def Search(request):
    query = request.GET.get('query', '')
    product = Product.objects.filter(name__icontains = query)
    context = {
        "products" :product,
    }
    return render(request, 'search.html', context)
