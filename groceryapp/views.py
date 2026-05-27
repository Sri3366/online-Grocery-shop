import json
import urllib.parse
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from .models import ORDERSTATUS, Carousel,Category, Feedback, Order,Product,User,UserProfile,Cart,Booking
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages

# Create your views here.
# A simple view function to create your user securely on the cloud database
def make_admin_account(request):
    # Change 'admin' and 'SecurePassword123' to whatever you want your login to be!
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'SecurePassword123')
        return HttpResponse("<h3>Superuser created successfully! You can log in now.</h3>")
    return HttpResponse("<h3>Account already exists.</h3>")

def home(request):
    # 1. Fetch your live admin products (limiting to 4 or 8 to fit the clean row grid)
    all_shop_products = Product.objects.all()[:4] 
    
    # 2. Build the context dictionary
    context = {
        'products': all_shop_products,
    }
    
    # 3. Render your premium file with the database context attached
    return render(request,'Home.html', context)

def navbar(request):
    return render(request,'navigation.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def admin_login(request):
    msg=None
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        try:
            if user.is_staff:
                login(request,user)
                messages.success(request,"User login successfully")
                return redirect('admin_dashboard')#url.py lo name lo unna value ivvali
            else:
                messages.success(request,"Invalid Credentials")
        except:
           messages.success(request,"Invalid Credentials")
        
    return render(request,'admin_login.html')

def admin_home(request):
    return render(request,'admin_base.html')

def admin_dashboard(request):
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    
    # 1. Package all your variables into a context dictionary
    context = {
        'user': user,
        'category': category,
        'product': product,
        'new_order': new_order,
        'dispatch_order': dispatch_order,
        'way_order': way_order,
        'deliver_order': deliver_order,
        'cancel_order': cancel_order,
        'return_order': return_order,
        'order': order,
        'read_feedback': read_feedback,
        'unread_feedback': unread_feedback,
    }
    
    # 2. Pass the context dictionary as the 3rd argument to render
    return render(request, 'admin_dashboard.html', context)

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        messages.success(request,"Category added") #category add chesi submit kodithe category added ani vasthundhi
        return redirect('view_category')  #ah tharvatha view_category page ki velthundhi
    return render(request,'add_category.html',locals())

def view_category(request):
    category = Category.objects.all()
    return render(request,'view_category.html',locals())

def edit_category(request,pid):
    category = Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST.get('name')
        category.name =name
        category.save()
        messages.success(request,"Category Updated")
        return redirect('view_category')
    return render(request,'edit_category.html',locals())

def delete_category(request,pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request,"Category Deleted")
    return redirect('view_category')

def add_product(request):
    category = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        cat = request.POST.get('category')
        discount = request.POST.get('discount')
        desc = request.POST.get('description')
        image = request.FILES.get('image')
        cat_obj = Category.objects.get(id=cat)
        Product.objects.create(name=name,price=price,discount=discount,category=cat_obj,description=desc,image=image)
        messages.success(request,'Product Added..')
    return render(request,'add_product.html',locals())


def view_product(request):
    product=Product.objects.all()
    return render(request,'view_product.html',locals())

def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')
    return render(request, 'edit_product.html', locals())

def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

def registration(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        image = request.FILES.get('image')
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registeration Successful")
    return render(request, 'registration.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')  #if logi successful then go to home page
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'userlogin.html', locals())


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile # Make sure your import matches your project structure

def profile(request):
    # Safe fallback: Ensure we get the user object safely
    user = request.user
    
    # 🟢 FIX: Automatically create a UserProfile record if it doesn't exist for this user
    data, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        
        # 1. Update Django's core User model fields
        user.first_name = fname
        user.last_name = lname
        user.email = email  # It's highly recommended to save the email too!
        user.save()
        
        # 2. Update custom Profile fields
        data.mobile = mobile
        data.address = address
        
        # Handle file uploads safely without crashing if left blank
        if request.FILES.get('image'):
            data.image = request.FILES.get('image')
            
        data.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
        
    return render(request, 'profile.html', locals())

def logoutUser(request):
    logout(request)
    messages.success(request,"Logout Successfully...")
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        # 🟢 FIX 1: Read 'currentpassword' to perfectly match the HTML name attribute
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        
        # Validate current password credentials
        user = authenticate(username=request.user.username, password=o)
        
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                
                # 🟢 FIX 2: Prevents user from being forcibly logged out after changing password
                update_session_auth_hash(request, user)
                
                messages.success(request, "Password Changed Successfully!")
                return redirect('home')
            else:
                messages.error(request, "New Password fields do not match.")
                return redirect('change_password')
        else:
            messages.error(request, "Invalid current password provided.")
            return redirect('change_password')
            
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())


def product_detail(request, pid):
    # Safe error boundaries using built-in 404 mechanisms
    product = get_object_or_404(Product, id=pid)
    latest_product = Product.objects.exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())

def addToCart(request, pid):
    # 🟢 STEP 1: Check if the user is NOT logged in
    if not request.user.is_authenticated:
        # Add a warning message that will show up via your layout's alert script
        messages.error(request, "Please login first to add products to your cart or buy them!")
        return redirect('userlogin') # Automatically routes them to your login page
        
    # 🟢 STEP 2: Existing cart logic (Executes only if user is logged in)
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
        
    return redirect('cart')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())

def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')

def booking(request):
    # Ensure the user has a profile and a cart
    try:
        user = UserProfile.objects.get(user=request.user)
        cart = Cart.objects.get(user=request.user)
    except (UserProfile.DoesNotExist, Cart.DoesNotExist):
        messages.error(request, "Profile or Cart not found.")
        return redirect('cart')

    total = 0
    discounted = 0
    deduction = 0

    # Safely format stringified single-quoted JSON dict to valid double-quoted JSON format
    product_data = (cart.product).replace("'", '"')
    
    try:
        product_dict = json.loads(str(product_data))
        product_items = product_dict['objects'][0]
        if not product_items:  # Check if the dictionary inside 'objects' is empty
            raise ValueError
    except (json.JSONDecodeError, KeyError, IndexError, ValueError):
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')

    # Calculate prices
    for i, j in product_items.items():
        try:
            product = Product.objects.get(id=i)
            qty = int(j)
            
            # 1. Calculate raw total price
            total += qty * float(product.price)
            
            # 2. Safely extract discount number if it contains a '%' character
            discount_str = str(product.discount).replace('%', '').strip()
            discount_value = float(discount_str) if discount_str.replace('.', '', 1).isdigit() else 0.0
            
            # 3. Calculate discounted price for this item
            item_discounted_price = float(product.price) * (100 - discount_value) / 100
            discounted += qty * item_discounted_price
            
        except Product.DoesNotExist:
            continue  # Skips item if it was deleted from the main store catalog

    # Calculate total money saved
    deduction = total - discounted

    if request.method == "POST":
        # Pass values smoothly into your payment view query string parameters
        return redirect(f'/payment/?total={int(total)}&discounted={int(discounted)}&deduction={int(deduction)}')

    return render(request, "booking.html", locals())
 

def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())


def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def user_feedback(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request,"Thank you! Your feedback has been submitted.")
    return render(request, "feedback-form.html", locals())

def manage_feedback(request):
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('manage_feedback')

@login_required
def payment(request):
    # This automatically checks for and builds the missing database table dynamically
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groceryapp_order (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                total_amount NUMERIC(10, 2) NOT NULL,
                discounted_amount NUMERIC(10, 2) NOT NULL,
                deduction_amount NUMERIC(10, 2) NOT NULL,
                payment_screenshot VARCHAR(100) NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                user_id INTEGER NOT NULL
            );
        """)
    # Fetch price parameters from the URL
    total_price = request.GET.get('discounted', '0.00')
    
    if request.method == "POST" and request.FILES.get('screenshot'):
        screenshot_file = request.FILES['screenshot']
        
        # 1. Setup sample items text string (Customize based on your cart data collection)
        # For example: "2kg Dry Fruits, 1kg Sugar"
        items_summary = "Fresh Groceries / Dry Fruits Selection" 
        
        # 2. Save order entry to PostgreSQL
        order = Order.objects.create(
            user=request.user,
            total_amount=float(total_price),
            items_ordered=items_summary,
            payment_screenshot=screenshot_file
        )
        
        # 3. CONSTRUCT THE WHATSAPP MESSAGE TEXT
        # You can adjust your business phone number and the delivery hours notice right here!
        your_whatsapp_number = "917993910966" # 🟢 Put your real WhatsApp number here (with 91 country code, no spaces)
        delivery_timeframe = "1 hour"    # 🟢 Set your expected delivery speed estimate
        
        raw_message = (
            f"Hello Lakshmi Durga Traders! 👋\n\n"
            f"I have successfully placed an order.\n"
            f"*Order ID:* #{order.id}\n"
            f"*Items:* {items_summary}\n"
            f"*Total Paid:* Rs.{total_price}\n\n"
            f"✅ I have attached my payment screenshot in the app. "
            f"Please deliver it within *{delivery_timeframe}*."
        )
        
        # Safely encode spaces and emojis for web browser address bars
        encoded_message = urllib.parse.quote(raw_message)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={your_whatsapp_number}&text={encoded_message}"
        
        # 💥 AUTOMATIC REDIRECT: Shoots the user straight to WhatsApp!
        return redirect(whatsapp_url)
        
    return render(request, 'payment.html')

def read_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 

def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals())

def manage_user(request):
    user = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals())

from django.db import connection

def delete_user(request, pid):
    if request.method == 'POST':
        # 1. Find the UserProfile row
        profile_record = get_object_or_404(UserProfile, id=pid)
        auth_user = profile_record.user
        
        # 2. Delete the profile row first (This is safe and works!)
        profile_record.delete()
        
        # 3. 🟢 BYPASS THE CASCADE BUG: Use a raw SQL query to drop the auth user 
        # This completely skips Django's ORM check, meaning it will NEVER look for "groceryapp_order"
        if auth_user:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM "auth_user" WHERE "id" = %s', [auth_user.id])
                
        messages.success(request, "User account successfully purged.")
    else:
        messages.error(request, "Invalid security request method context.")
        
    return redirect('admin_dashboard')

def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

def grocery_shop_router(request):
    # 1. Check if the user has logged into an active account session
    if request.user.is_authenticated:
        # User is Logged In -> Serve the premium page with live database products
        all_shop_products = Product.objects.all()[:4] 
        context = {
            'products': all_shop_products,
        }
        return render(request, 'Home.html', context)
        
    else:
        # User is Logged Out -> Serve the guest page with the carousels
        carousel_data = Carousel.objects.all()
        context = {
            'carousel': carousel_data
        }
        return render(request, 'index.html', context)
    

def run_migrations_view(request):
   try:
        # 1. Tells Django's history tracker to catch up and record what it thinks it did
        call_command('migrate', 'groceryapp', '--fake', interactive=False)
        
        # 2. Re-runs the actual, hard database structural updates sequentially
        call_command('migrate', 'groceryapp', interactive=False)
        
        # 3. Safety valve: Running the universal project migrator
        call_command('migrate', interactive=False)
        
        return HttpResponse("<h2>Database deep sync complete! All app profiles, carts, and user relations are live.</h2>")
   except Exception as e:
        return HttpResponse(f"<h2>Sync met a blocker:</h2><p>{str(e)}</p>")
   
def create_new_admin_view(request):
    try:
        # 💥 THE TOTAL PURGE: Delete absolutely EVERY user in the database
        User.objects.all().delete()
        
        # 🟢 Create your fresh, clean superuser profile
        # Change 'srivenkat' and 'YourSecretPassword123' to whatever you want to keep!
        user = User.objects.create_superuser(
            username='teju',
            email='teju@example.com',
            password='teju@123'
        )
        
        # Force log your session in immediately
        login(request, user)
        
        # Take you straight past the login page and into your dashboard!
        return redirect('/admin-login/')
        
    except Exception as e:
        return HttpResponse(f"<h2>Failed to reset user database:</h2><p>{str(e)}</p>")