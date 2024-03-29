from django.shortcuts import render,redirect
import calendar
from .models import *;
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import *;
from django.db.models.functions import ExtractMonth
from django.contrib.auth import *;
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.db.models import *

# Create your views here.
def home(request):
    banners = Banner.objects.all().order_by('-id')
    data = Product.objects.filter(is_featured = True).order_by('-id')
    context = {'data': data,
               'banners':banners
              }
    return render(request , 'index.html',context)
#Category
def category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})
#Brand
def brand_list(request):
    brand = Brand.objects.all().order_by('-id')
    context = {'data': brand}
    return render(request,'brand_list.html',context)
#product_list
def product_list(request):
    data= Product.objects.all().order_by('-id')
    context = { 'data': data,
              }
    return render(request,'product_list.html',context)
#product list according to category


def category_product_list(request,cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')
    context = {'data':data}
    return render(request , 'category_product_list.html',context)

def brand_product_list(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    context = {'data':data}
    return render(request,'brand_product_list.html',context)




#product-details

def product_detail(request,slug,id):
    product = Product.objects.get(id=id)
    related_product = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    reviewForm = ReviewAdd()
    canAdd = True
  
    if request.user.is_authenticated:
        reviewCheck = ProductReview.objects.filter(user = request.user,product = product).count()
        if reviewCheck > 0:
            canAdd = False
    reviews = ProductReview.objects.filter(product = product)

    

    context = {'data':product,
               'related':related_product,
               'reviewForm':reviewForm,
                'canAdd' : canAdd,
                'reviews':reviews,
              
            }
    return render(request,'product_detail.html',context)

#search
def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    context = {'data': data,
              }
    return render(request , 'search.html',context)



def add_to_cart(request):
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'price':request.GET['price'],
        'qty':request.GET['qty'],
        'image':request.GET['image'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

def cart_list(request):
    total_amt = 0
    context = {}
    if 'cartdata' in request.session:
        for p_id , items in request.session['cartdata'].items():
            total_amt += int(items['qty']) * float(items['price'])       
        context = {
            'cart_data':request.session['cartdata'],
            'totalitems':len(request.session['cartdata']),
            'total_amt':total_amt

        }
    return render(request,'cart.html',context)

def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data

            
    total_amt = 0
    for p_id , items in request.session['cartdata'].items():
        total_amt += int(items['qty']) * float(items['price'])
        
    totalitems=len(request.session['cartdata'])
    return JsonResponse({'bool':True,'totalitems':totalitems,'total_amt':total_amt})



#update cart
def update_cart(request):
    id = str(request.GET['p_id'])
    qty = request.GET['qty']
    cart_data = request.session['cartdata']
    if 'cartdata' in request.session:
        cart_data[id]['qty'] = qty
        cart_data.update(cart_data)
        request.session['cartdata'] = cart_data

    total_amt = 0
    for p_id , items in request.session['cartdata'].items():
        total_amt += int(items['qty']) * float(items['price'])
        
    item_amt =  int(cart_data[id]['qty'])* float(cart_data[id]['price'])
   
    return JsonResponse({'bool':True,'total_amt':total_amt,'item_amt':item_amt})


def signup(request):
    form = SignupForm
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(request,username=username, password=pwd)
            login(request, user)
            return redirect('home')
    
    context = {
        'form':form
    }
    return render(request,'registration/singup.html',context)




# without authenticatetion we can't open this checkout page
@login_required  
def checkout(request):
    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        #Order 
        for p_id , items in request.session['cartdata'].items():
            totalAmt += int(items['qty']) * float(items['price'])

        order = CartOrder.objects.create(
            user = request.user,
            total_amt = totalAmt,
        )
        total_amt = totalAmt
        for p_id , items in request.session['cartdata'].items():
            items = CartOrderItems.objects.create(
                order = order,
                invoice_no = 'INV-'+str(order.id),
                item = items['title'],
                image = items['image'],
                qty = items['qty'],
                price = items['price'],
                total = float(items['qty'])*float(items['price'])
            )
        host = request.get_host()
        paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': total_amt,
                'item_name': 'OrderNo-'+str(order.id),
                'invoice': 'INV-'+str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
            }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address = UserAddressBook.objects.filter(user=request.user,status=True).first()

    context = {
        'cart_data':request.session['cartdata'],
        'totalitems':len(request.session['cartdata']),
        'total_amt':total_amt,
        'form':form,
        'address':address

    }
    return render(request,'checkout.html',context)




@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')

#save Review
def save_review(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review_text = request.POST['review_text'],
        review_rating = request.POST['review_rating'],
    )
    data = {
        'user':user.username,
        'review_text':request.POST['review_text'],
        'review_rating': request.POST['review_rating'],
    }
    avg_reviews = ProductReview.objects.filter(product = product).aaggregate(avg_rating=Avg('review_rating'))
    return JsonResponse({'bool':True,'data':data,'  avg_reviews':  avg_reviews})

        
def my_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values(
        'month'
    ).annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])

    context = {
        'monthNumber':monthNumber,
         'totalOrders':totalOrders
    }
    return render(request,'user/dashboard.html',context)

def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user)
    context = {
        'orders':orders,
    }
    return render(request,'user/orders.html',context)

def my_order_items(request,id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    context = {
       'orderitems':orderitems,
    }

    return render(request , 'user/order-items.html',context)



def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    user = request.user
    data = {}
    if user.is_authenticated:
        checkw = Wishlist.objects.filter(product=product,user=user).count()
        if checkw > 0:
            data = {
                'bool':False
            }
        else:
            wishlist = Wishlist.objects.create(
                product = product,
                user = user
            )
            data = {
                'bool':True
            }

    return JsonResponse(data)

def my_wishlist(request):
    user = request.user
    if user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=user)
        context={
            'wlist':wishlist
        }
    return render(request,"user/wishlist.html",context)


def my_reviews(request):
    user = request.user
    if user.is_authenticated:
        reviews = ProductReview.objects.filter(user = user)
    return render(request,"user/reviews.html",{'reviews':reviews})

def my_addressbook(request):
    user = request.user
    addbook = UserAddressBook.objects.filter(user=user)
    return render(request,"user/addressbook.html",{'addbook':addbook})


def save_address(request):
    form = AdressBookForm
    msg = None
    if request.method == 'POST':
        form = AdressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            form.save()
            msg = 'Data has been saved'
    return render(request,"user/add-address.html",{'form':form,'msg':msg})

def activate_address(request):
    aid = request.GET['id']
    UserAddressBook.objects.update(status=False)
    AddressBook = UserAddressBook.objects.get(pk=aid)
    AddressBook.status = True
    AddressBook.save()
    return JsonResponse({'bool':True})

def edit_profile(request):
    msg = None
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Data has been saved'
    form = ProfileForm(instance=request.user)
    return render(request,"user/edit-profile.html",{'form':form,'msg':msg})

def edit_addressBook(request,id):
    addressBook = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AdressBookForm(request.POST,instance=addressBook)
        if form.is_valid():
            if 'status' in request.POST:
               UserAddressBook.objects.update(status=False)
            form.save()
            msg = 'Data has been saved'
    form = AdressBookForm(instance=addressBook)
    return render(request,"user/update-address.html",{'form':form,'msg':msg})