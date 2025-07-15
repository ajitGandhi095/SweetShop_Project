from django.shortcuts import render, redirect, get_object_or_404
from EApp.models import *
from EApp.forms import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from datetime import datetime, timedelta
import uuid

# Create your views here.

def product_view(request):
    product_list= ProductModel.objects.all()

    my_dict= {'products':product_list}
    return render(request, "EApp/index.html", my_dict)

def about_view(request):
    return render(request, 'EApp/about.html')

def contact_view(request):
    return render(request, 'EApp/contact.html')

def shop_view(request, category=None):
    product_list= ProductModel.objects.all()

    my_dict= {'products':product_list}
    return render(request, 'EApp/shop.html', my_dict)

def signup_view(request):
    if request.method == "POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            #Hash the password before saving
            row_password= form.cleaned_data.get('password')
            user.password= make_password(row_password)
            user.cpassword= ''
            user.save()
            messages.success(request, "Signup Successfull, Please Login")
            return redirect('login')
    else:
        form= SignUpForm()

    my_dict= {'form':form}
    return render(request, 'EApp/signup.html', my_dict)

def login_view(request):

    if request.method == "POST":
        form= LoginForm(request.POST)
        if form.is_valid():
            email= request.POST.get('email')
            raw_password= request.POST.get('password')
            try:
                user= SignupModel.objects.get(email=email)
                if check_password(raw_password, user.password):
                    request.session['user_id']= user.id
                    request.session['is_admin']= user.is_admin
                    messages.success(request, "Login Successfull")
                    return redirect('homepage')
                else:
                    messages.error(request, "Invalid Password")

            except SignupModel.DoesNotExist:
                messages.error(request, "Invalid Email")

    else:
        form= LoginForm()
    return render(request, 'EApp/login.html', {'form':form})

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out")
    return redirect('home')

def home_view(request):
    product_list= ProductModel.objects.all()

    my_dict= {'products':product_list}
    return render(request, 'EApp/home.html', my_dict)

def home_about_view(request):
    return render(request, 'EApp/home_about.html')

def home_contact_view(request):
    return render(request, 'EApp/home_contact.html')

def home_shop_view(request):
    product_list= ProductModel.objects.all()

    my_dict= {'products':product_list}
    return render(request, 'EApp/home_shop.html', my_dict)

def add_to_cart_view(request, id):
    user_id= request.session.get('user_id')
    user= SignupModel.objects.get(id=user_id)
    product= ProductModel.objects.get(id=id)
    cart_item, created= CartItemModel.objects.get_or_create(product=product, user=user)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('view_cart_item')

def view_cart(request):
    user_id= request.session.get('user_id')
    user= SignupModel.objects.get(id=user_id)
    cart_items= CartItemModel.objects.filter(user=user.id)
    total_price= sum(item.product.price * item.quantity for item in cart_items)
    cart_count= sum(item.quantity for item in cart_items)

    my_dict= {'cart_items':cart_items, 'total_price':total_price, 'cart_count':cart_count}
    return render(request, 'EApp/home_cart.html', my_dict)

def remove_from_cart(request, id):
    user_id= request.session.get('user_id')
    user= SignupModel.objects.get(id=user_id)
    cart_item= CartItemModel.objects.get(id=id, user=user.id)
    cart_item.delete()
    return redirect('view_cart_item')

# def cart_count_processor(request):
#     if request.session.get('user_id'):
#         try:
#             user = SignupModel.objects.get(id=request.session.get('user_id'))
#             cart_items = CartItemModel.objects.filter(user=user)
#             cart_count = sum(item.quantity for item in cart_items)
#             return {'cart_count': cart_count}
#         except:
#             return {'cart_count': 0}
#     return {'cart_count': 0}

def useraccount_view(request):
    user_id= request.session.get('user_id')
    user= SignupModel.objects.get(id=user_id)
    username= user.name
    date= datetime.now()
    msg= ""
    h=date.hour

    if h<12:
        msg += "Good  Morning"
    elif h<16:
        msg += "Good Afternoon"
    elif h<20:
        msg += "Good Evening"
    else:
        msg += "Good Night"

    my_dict= {'date':date.strftime("%H:%M:%S"), 'msg':msg, 'username':username}
    return render(request, 'EApp/user_profile.html', my_dict)

def admin_login(request):

    if request.method == "POST":
        form= AdminLogin(request.POST)
        email= request.POST.get("email", "").strip()
        password= request.POST.get("password", "")

        try:
            user= SignupModel.objects.get(email=email)

            if check_password(password, user.password):
                if user.is_admin:
                    request.session['user.id']= user.id
                    request.session['is_admin']= True
                    return redirect('admin-dashboard')
                else:
                    messages.error(request, "You are not admin")
            else:
                messages.error(request, "Invalid Password")

        except SignupModel.DoesNotExist:
            messages.error(request, "Invalid Email")

    else:
        form= AdminLogin()

    return render(request, "EApp/admin_login.html", {'form':form})

def admin_dashboard_view(request):
    user_id= request.session.get('user_id')
    user= SignupModel.objects.get(id=user_id)
    username= user.name
    date= datetime.now()
    msg= ""
    h=date.hour

    if h<12:
        msg += "Good  Morning"
    elif h<16:
        msg += "Good Afternoon"
    elif h<20:
        msg += "Good Evening"
    else:
        msg += "Good Night"

    if not request.session.get('is_admin'):
        messages.error(request, "You must be an admin to access this page")
        return redirect('admin-login')
    
    #Create New Sweets
    
    if request.method == "POST":
        form= ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product= form.save()
            messages.success(request, "'{}'New Sweet Created Successfully...".format(product.name)) 
        else:
            messages.error(request, "Product Added Failed")
        return redirect('admin-dashboard')

    else:
        form=ProductForm()

    #Retrieve Product List
    product_list= ProductModel.objects.all()

    #Retrive all Signup User details
    user_list= SignupModel.objects.all()

    #Display All Orders with related user
    order_list= OrderModel.objects.select_related('user', 'delivery_address', 'payment').all()
    

    my_dict= {'date':date.strftime("%H:%M:%S"),'username':username, 'msg':msg, 'form':form, 'product_list':product_list, 'user_list':user_list, 'order_list':order_list}
    
    return render(request, "EApp/admin_dashboard.html", my_dict)

# In admin-dashboard Delete Existing Sweets
def product_delete_view(request, id):
    product= ProductModel.objects.get(id=id)
    product.delete()
    messages.success(request, "'{}' Deleted Successfully...".format(product.name))
    return redirect('admin-dashboard')

# In admin-dashboard Update Existing Sweets
def product_update_view(request, id):
    product= ProductModel.objects.get(id=id)
    # form= ProductForm(instance=product)

    if request.method == "POST":
        form=ProductForm(request.POST , request.FILES, instance=product)
        if form.is_valid():
            product= form.save()
            messages.success(request, "'{}' Updated Successfully...".format(product.name))
            return redirect('admin-dashboard')
        else:
            messages.error(request, "'{}' Update Failed".format(product.name))
    else:
        form= ProductForm(instance=product)

    # Rebuild dashboard context
    date = datetime.now()
    h = date.hour
    msg = (
        "Good Morning" if h < 12 else
        "Good Afternoon" if h < 16 else
        "Good Evening" if h < 20 else
        "Good Night"
    )

    product_list = ProductModel.objects.all()
    user_list = SignupModel.objects.all()

    my_dict= {'date':date.strftime("%H:%M:%S"), 'msg':msg, 'form':form, 'product_list':product_list, 'user_list':user_list}
        
    return render(request, 'EApp/admin_dashboard.html', my_dict)

# In admin dashboard delete existing user
def user_delete_view(request, id):
    user_to_delete= get_object_or_404(SignupModel, id=id)
    current_user_id= request.session.get('user_id')

    #Prevent Self-deletion
    if user_to_delete.id == current_user_id:
        messages.warning(request, 'You cannot delete your own admin account.')
        return redirect('admin-dashboard')
    
    user_to_delete.delete()
    messages.success(request, "'{}' Deleted Successfully".format(user_to_delete.name))
    return redirect('admin-dashboard')


def checkout_view(request):
    user_id= request.session.get('user_id')
    user= SignupModel.objects.get(id=user_id)
    cart_items= CartItemModel.objects.filter(user=user.id)
    total_price= sum(item.product.price * item.quantity for item in cart_items)
    cart_count= sum(item.quantity for item in cart_items)

    form= CheckoutForm()
    if request.method == "POST":
        form= CheckoutForm(request.POST)
        if form.is_valid():
            checkout_instance= form.save(commit=False)
            checkout_instance.user= user
            checkout_instance.save()

            request.session['delivery_address_id'] = checkout_instance.id
            request.session['total_price'] = float(total_price)
            return redirect('payment_page')
    
    my_dict= {'form':form, 'total_price':total_price, 'cart_count':cart_count}
    return render(request, 'EApp/checkout.html', my_dict)

def get_expected_delivery_date(pincode):
    # Map pincodes to estimated delivery days
    delivery_days_by_pincode = {
        '560001': 2,  # Bangalore
        '110001': 3,  # Delhi
        '400001': 4,  # Mumbai
        # Add more if needed
    }
    # Default to 5 days if not found
    days = delivery_days_by_pincode.get(pincode, 5)
    expected_date = datetime.today() + timedelta(days=days)
    
    return expected_date.date() # Example: Monday, July 15

def paymentpage_view(request):
    user_id = request.session.get('user_id')
    user = SignupModel.objects.get(id=user_id)
    total_price= request.session.get('total_price', 0)

    expected_delivery= None
    address= None

    # Get Selected Delivery address
    address_id = request.session.get('delivery_address_id')
    if address_id:
        address = DeliveryAddressModel.objects.filter(id=address_id).first()
        if address:
            expected_delivery = get_expected_delivery_date(address.pincode)

    if request.method == 'POST':
        method= request.POST.get('payment_method')
        transaction_id = f"TXN{user_id}{str(uuid.uuid4())[:8]}"

        if method == 'upi':
            upi_id = request.POST.get('upi_id')
            # (You can validate UPI format here)
            payment_status = 'Success'

        elif method == 'card':
           card_number= request.POST.get('card_number')
           expiry= request.POST.get('expiry')
           cvv= request.POST.get('cvv')
           payment_status= "Success"

        elif method == 'netbanking':
           bank= request.POST.get('bank')
           payment_status= "Success"

        elif method == 'cod':
           payment_status= 'Pending'
           transaction_id= None
        else:
           messages.error(request, "Invalid Payment Method")
           return redirect('payment_page')

        # Save to paymentmodel
        payment= PaymentModel.objects.create(
           user= user,
           amount= total_price,
           payment_status= payment_status,
           transaction_id= transaction_id
        )

        # ✅ Then save order with address and expected delivery
        if address and expected_delivery:
            OrderModel.objects.create(
                user=user,
                delivery_address=address,
                payment=payment,
                expected_delivery_date=expected_delivery,
                status="Processing"
            )

        # Clear user's cart after successful payment
        CartItemModel.objects.filter(user=user.id).delete()

        if payment_status == "Success":
            messages.success(request, "Payment Successfull")
        else:
            messages.success(request, 'Order placed with case on delivary')

        return redirect('payment_success')
           
    my_dict= {'total_price':total_price, 'expected_delivery':expected_delivery}
    return render(request, 'EApp/payment.html', my_dict)

def paymentsuccess_view(request):
    user_id= request.session.get('user_id')

    # Get the latest payment by this user
    payment = PaymentModel.objects.filter(user_id=user_id).order_by('-timestamp').first()

    # Get the delivery address if stored in session
    address = None
    expected_delivery= None
    address_id = request.session.get('delivery_address_id')
    if address_id:
        address = DeliveryAddressModel.objects.filter(id=address_id).first()
        if address:
            expected_delivery= get_expected_delivery_date(address.pincode)

    my_dict= {'payment':payment, 'address':address, 'expected_delivery':expected_delivery}
    return render(request, 'EApp/payment_success.html', my_dict)