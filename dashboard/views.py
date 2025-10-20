# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Product, Wishlist


# ======================================================================
# 🏠 HOME PAGE — Displays all products
# ======================================================================
@never_cache
@login_required
def home(request):
    products = Product.objects.all().order_by('-created_at')
    print(request.user)  # Debug: show logged-in user
    return render(request, 'home.html', {'products': products})


# ======================================================================
# 🛒 SELL PRODUCT — Create new product listing
# ======================================================================
@login_required
def sell_product(request):
    if request.method == 'POST':
        try:
            # Create new product instance
            product = Product(
                user=request.user,
                name=request.POST.get('name'),
                price=request.POST.get('price'),
                category=request.POST.get('category'),
                description=request.POST.get('description'),
                location=request.POST.get('location'),
                floor=request.POST.get('floor'),
                room_number=request.POST.get('room_number'),
                wing=request.POST.get('wing'),
                contact_number=request.POST.get('contact_number'),
                academic_year=request.POST.get('academic_year'),
            )

            # Handle image upload
            if 'image' in request.FILES and request.FILES['image']:
                product.image = request.FILES['image']

            product.save()
            return redirect('dashboard_home')

        except Exception as e:
            print(f"❌ Error creating product: {e}")
            return render(request, 'sell.html', {
                'error': 'There was an error while creating your product. Please try again.'
            })

    # GET request — show empty form
    return render(request, 'sell.html')


# ======================================================================
# 💖 TOGGLE WISHLIST — Add/Remove products to user's wishlist (AJAX)
# ======================================================================
@login_required
def toggle_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()
            status = "removed"
        else:
            Wishlist.objects.create(user=request.user, product=product)
            status = "added"

        return JsonResponse({"status": status, "product_id": product.id})

    return JsonResponse({"error": "Invalid request"}, status=400)


# ======================================================================
# 📜 WISHLIST VIEW — Show all wishlisted products
# ======================================================================
@login_required
def wishlist_view(request):
    wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    wishlist_products = Product.objects.filter(id__in=wishlist_product_ids)

    # Add attribute for template (to glow heart icon)
    for product in wishlist_products:
        product.wishlisted = True

    return render(request, 'wishlist.html', {'products': wishlist_products})


# ======================================================================
# ❌ DELETE FROM WISHLIST — Remove item via AJAX
# ======================================================================
@require_POST
@login_required
def delete_from_wishlist(request):
    product_id = request.POST.get('product_id')

    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'Missing product ID'}, status=400)

    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({'status': 'deleted'})


# ======================================================================
# 🔍 FILTER PRODUCTS — Filter by category, location, floor, and price
# ======================================================================
def filter(request):
    products = Product.objects.filter(is_active=True)

    if request.method == "POST":
        categories = request.POST.getlist('category')
        locations = request.POST.getlist('location')
        floors = request.POST.getlist('floor')
        price = request.POST.get('price')

        # Apply filters dynamically
        if categories:
            products = products.filter(category__in=categories)
        if locations:
            products = products.filter(location__in=locations)
        if floors:
            products = products.filter(floor__in=floors)
        if price:
            try:
                products = products.filter(price__lte=float(price))
            except ValueError:
                pass  # ignore invalid price

    return render(request, 'filter.html', {'products': products})


# ======================================================================
# 🧾 PRODUCT DETAIL PAGE — Show full info of a product
# ======================================================================
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Increment view count
    product.views += 1
    product.save()

    return render(request, 'product.html', {'product': product})


# ======================================================================
# 📦 MY PRODUCTS — Show products uploaded by the current user
# ======================================================================
@login_required
def my_products(request):
    products = Product.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'my_products.html', {'products': products})


# ======================================================================
# ⚙️ MANAGE PRODUCT — Edit or delete existing products
# ======================================================================
@login_required
def manage_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # DELETE PRODUCT
        if 'delete_product' in request.POST:
            product.delete()
            messages.success(request, f'Product "{product.name}" has been deleted.')
            return redirect('dashboard_home')

        # UPDATE PRODUCT
        elif 'update_product' in request.POST:
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.category = request.POST.get('category')
            product.location = request.POST.get('location')
            product.floor = request.POST.get('floor')
            product.room_number = request.POST.get('room_number')
            product.block = request.POST.get('block')
            product.location_details = request.POST.get('location_details')

            if request.FILES.get('image'):
                product.image = request.FILES['image']

            product.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('manage_product', product_id=product.id)

    return render(request, 'manage_product.html', {'product': product})


# ======================================================================
# 🚪 LOGOUT VIEW — Logs user out and clears session
# ======================================================================
@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')










@login_required
def delete_product_ajax(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        try:
            product = Product.objects.get(id=product_id, user=request.user)
            product.delete()
            return JsonResponse({"status": "success"})
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})





from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.academic_year = request.POST.get("academic_year")
        product.category = request.POST.get("category")
        product.location = request.POST.get("location")
        product.floor = request.POST.get("floor")
        product.room_number = request.POST.get("room_number")
        product.wing = request.POST.get("wing")
        product.contact_number = request.POST.get("phone_number")

        # Handle image update if uploaded
        if request.FILES.get("image"):
            product.image = request.FILES["image"]

        product.save()
        return redirect("my_products")  # redirect back to product list

    # In case GET request, just redirect
    return redirect("my_products")




from django.shortcuts import render
from .models import Product

from django.shortcuts import render
from .models import Product

def filter_products(request):
    products = Product.objects.all()  # Start with all products

    if request.method == "POST":
        # Get comma-separated values from hidden inputs
        categories = request.POST.get('categories', '')  # e.g., "books,electronics"
        locations = request.POST.get('locations', '')
        floors = request.POST.get('floors', '')

        # Convert to lists
        category_list = categories.split(',') if categories else []
        location_list = locations.split(',') if locations else []
        floor_list = floors.split(',') if floors else []

        # Filter products based on selections
        if category_list:
            products = products.filter(category__in=category_list)
        if location_list:
            products = products.filter(location__in=location_list)
        if floor_list:
            products = products.filter(floor__in=floor_list)

    return render(request, 'filter.html', {'products': products})









from django.http import JsonResponse
from .models import Product

def search_products_ajax(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)

    # Prepare product data to send as JSON
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'category': product.get_category_display(),
            'location': product.get_location_display(),
            'floor': product.get_floor_display(),
            'image_url': product.image.url if product.image else '',
        })

    return JsonResponse({'products': products_list})
