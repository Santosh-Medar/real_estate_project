from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#Index Page View
def home(request):
    return render(request, 'core/index.html')

#Landing pages Views
def seller_landing_page(request):
    return render(request, 'core/seller/landing_page.html')

def buyer_landing_page(request):
    return render(request, 'core/buyer/landing_page.html')

def admin_landing_page(request):
    return render(request, 'core/admin/landing_page.html')

#Registration Views
def buyer_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'core/buyer/register.html')

        # Check if email already exists (optional but good)
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'core/buyer/register.html')

        # Create buyer user
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='buyer'
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect('buyer_login')

    return render(request, 'core/buyer/register.html')

def seller_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'core/seller/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'core/seller/register.html')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='seller'
        )
        messages.success(request, "Registration successful! Please log in.")
        return redirect('seller_login')

    return render(request, 'core/seller/register.html')

#Login Views
def buyer_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user and user.role == 'buyer':
            login(request, user)
            return redirect('buyer_dashboard')   # success
        else:
            return render(request, 'core/buyer/login.html', {'error': 'Invalid buyer credentials'})
    
    return render(request, 'core/buyer/login.html')

def seller_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user and user.role == 'seller':
            login(request, user)
            return redirect('seller_dashboard')   # success
        else:
            return render(request, 'core/seller/login.html', {'error': 'Invalid seller credentials'})
    
    return render(request, 'core/seller/login.html')

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user and (user.role == 'admin' or user.is_superuser):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'core/admin/login.html', {'error': 'Invalid admin credentials'})

    return render(request, 'core/admin/login.html')

@login_required
def logout_view(request):
    user = request.user
    logout(request)  # clear session

    # redirect based on role
    if user.is_superuser:
        return redirect('admin_landing_page')
    elif user.role == 'seller':
        return redirect('seller_landing_page')
    elif user.role == 'buyer':
        return redirect('buyer_landing_page')

    return redirect('home')  # fallback


def redirect_based_on_role(user):
    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard') # Or custom admin_dashboard
    elif user.role == 'seller':
        return redirect('seller_dashboard')
    else:
        return redirect('buyer_dashboard')

@login_required
def buyer_dashboard(request):
    approved_properties = Property.objects.filter(status='approved')
    return render(request, 'core/buyer/dashboard.html', {'properties': approved_properties})

def all_properties_api(request):
    properties = Property.objects.filter(status="Approved") 

    data = []
    print(properties)

    for p in properties:
        data.append({
            "id": p.id,
            "price": float(p.price),
            "location": p.address,
            "type": p.title,
            "beds": getattr(p, "beds", "-"),
            "baths": getattr(p, "baths", "-"),
            "sqft": getattr(p, "sqft", "-"),
            "image": p.image.url if p.image else "/static/default.jpg"
        })

    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def admin_dashboard(request):
    # Security: Only Admins allowed
    if request.user.role != 'admin': 
        return redirect('login')
    
    pending_count = Property.objects.filter(status="Pending").count()
    approved_count = Property.objects.filter(status="approved").count()
    buyer_count = User.objects.filter(role="buyer").count()
    seller_count = User.objects.filter(role="seller").count()

    data = {
        "pending": pending_count,
        "approved": approved_count,
        "buyers": buyer_count,
        "sellers": seller_count
    }
    # Fetch only Pending properties
    pending_properties = Property.objects.filter(status='pending').order_by('-created_at')
    
    # Optional: Fetch all users to show stats
    total_users = User.objects.count()
    
    return render(request, 'core/admin/dashboard.html', {
        'pending_properties': pending_properties,
        'total_users': total_users,
        'data': data
    })

@login_required(login_url='login')
def seller_dashboard(request):
    if request.user.role != 'seller': 
        return redirect('login')
    
    return render(request, 'core/seller/dashboard.html')

def seller_properties_api(request):
    seller = request.user
    properties = Property.objects.filter(seller=seller)

    data = []

    for p in properties:
        data.append({
            "id": p.id,
            "price": float(p.price),
            "location": p.address,
            "status": p.status.title(),
            "beds": getattr(p, "beds", "-"),
            "baths": getattr(p, "baths", "-"),
            "sqft": getattr(p, "sqft", "-"),
            "image": p.image.url if p.image else "/static/default.jpg"
        })

    return JsonResponse(data, safe=False)

@csrf_exempt   # optional if you manually send CSRF token from JS
def delete_property_api(request, id):
    if request.method == "POST":
        prop = Property.objects.filter(id=id, seller=request.user).first()

        if not prop:
            return JsonResponse({"success": False, "error": "Property not found"}, status=404)

        prop.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

@login_required(login_url='login')
def add_property(request):
    if request.method == 'POST':

        # 1. Get Form Text Fields
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        property_type = request.POST.get('property_type')
        city = request.POST.get('city')
        address = request.POST.get('address')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')

        # 2. Image Upload
        image = request.FILES.get('image')

        # 3. Create Property Object
        Property.objects.create(
            seller=request.user,
            title=title,
            price=price,
            description=description,
            property_type=property_type,
            city=city,
            address=address,
            image=image,
            contact_phone=contact_phone,
            contact_email=contact_email,
            status='Pending'
        )

        return redirect('seller_dashboard')
    
    return render(request, 'core/seller/add_property.html')

@login_required(login_url='login')
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    # Ensure only the owner can edit
    if property_obj.seller != request.user:
        return redirect('seller_dashboard')

    if request.method == 'POST':
        property_obj.title = request.POST.get('title')
        property_obj.price = request.POST.get('price')
        property_obj.description = request.POST.get('description')
        property_obj.property_type = request.POST.get('property_type')
        property_obj.city = request.POST.get('city')
        property_obj.address = request.POST.get('address')
        property_obj.contact_phone = request.POST.get('contact_phone')
        property_obj.contact_email = request.POST.get('contact_email')

        # Update image if a new one is provided
        if 'image' in request.FILES:
            property_obj.image = request.FILES['image']

        property_obj.save()
        return redirect('seller_dashboard')

    return render(request, 'core/seller/edit_property.html', {'property': property_obj})

@login_required(login_url='login')
def approve_property(request, pk):
    if request.user.role == 'admin':
        property_obj = Property.objects.get(pk=pk)
        property_obj.status = 'Approved'
        property_obj.save()
    return redirect('admin_dashboard')

@login_required(login_url='login')
def reject_property(request, pk):
    if request.user.role == 'admin':
        property_obj = Property.objects.get(pk=pk)
        property_obj.status = 'Rejected'
        property_obj.save()
    return redirect('admin_dashboard')

@login_required(login_url='login')
def delete_property(request, pk):
    try:
        property_obj = Property.objects.get(pk=pk)
        # Security: Ensure only the owner can delete
        if property_obj.seller == request.user:
            property_obj.delete()
    except Property.DoesNotExist:
        pass
        
    return redirect('seller_dashboard')

@login_required(login_url='login')
def property_detail(request, pk):
    # Get the property or show 404 error if not found
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Optional: If you want to restrict this page only to approved properties (unless it's the owner/admin)
    if property_obj.status != 'approved' and request.user.role == 'buyer':
        return redirect('buyer_dashboard')

    return render(request, 'core/seller/property_detail.html', {'property': property_obj})

def pending_properties(request):
    if request.user.role != 'admin': 
        return redirect('login')
    
    pending_properties = Property.objects.filter(status='Pending').order_by('-created_at')
    
    return render(request, 'core/admin/pending_properties.html', {
        'pending_properties': pending_properties
    })

def view_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    # ADMIN VIEW
    if request.user.role == 'admin':
        return render(request, 'core/admin/property_view.html', {
            'property': property_obj
        })

    # SELLER VIEW
    if request.user.role == 'seller':
        return render(request, 'core/seller/property_detail.html', {
            'property': property_obj
        })
    
    # BUYER VIEW (optional)
    return render(request, 'core/buyer/property_detail.html', {
        'property': property_obj
    })

@login_required(login_url='login')
def remove_property(request, id):
    if request.method == "POST":
        try:
            prop = Property.objects.get(id=id)
            prop.status = "Pending"
            prop.save()
            return JsonResponse({"success": True})
        except Property.DoesNotExist:
            return JsonResponse({"success": False, "error": "Property not found"}, status=404)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
