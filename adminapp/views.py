from django.shortcuts import render

# Create your views here.

# def index(request):
#     return render(request, 'index.html')
from django.utils.timezone import now, timedelta
from userapp.models import tbl_register
from userapp.models import ProductBooking, Cart

def index(request):

    # 1️⃣ Count of active users
    active_users = tbl_register.objects.count()

    # 2️⃣ Count products sold = single product orders + cart quantities
    single_orders_count = ProductBooking.objects.all().count()
    cart_items_count = Cart.objects.filter(status="completed").count()

    products_sold = single_orders_count + cart_items_count

    # 3️⃣ Count users registered in last 7 days
    seven_days_ago = now() - timedelta(days=7)
    new_signups = tbl_register.objects.filter(
        created_at__gte=seven_days_ago
    ).count() if hasattr(tbl_register, 'created_at') else 0

    return render(request, "index.html", {
        "active_users": active_users,
        "products_sold": products_sold,
        "new_signups": new_signups,
    })


def calendar(request):
    return render(request, 'calendar.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import tbl_admin  # make sure tbl_admin exists

def login(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        try:
            admin = tbl_admin.objects.get(password=password,username=username)
            request.session['admin_id'] = admin.id
            return render(request, 'index.html')  # on successful login
        except tbl_admin.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')  # on error
    return render(request, 'login.html')  # for GET request

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category

def category_page(request):
    cat_id = request.GET.get("edit")  # For editing
    categories = Category.objects.all()

    # ---- EDIT MODE ----
    if cat_id:
        category_instance = get_object_or_404(Category, id=cat_id)

        if request.method == "POST":
            category_instance.name = request.POST.get("name")
            category_instance.save()
            return redirect("category_page")

        return render(request, "category_page.html", {
            "categories": categories,
            "edit_mode": True,
            "category": category_instance
        })

    # ---- ADD MODE ----
    if request.method == "POST":
        name = request.POST.get("name")
        Category.objects.create(name=name)
        return redirect("category_page")

    return render(request, "category_page.html", {
        "categories": categories,
        "edit_mode": False
    })


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect("category_page")
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category

def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        category = get_object_or_404(Category, id=category_id)

        name = request.POST.get("name")
        description = request.POST.get("description")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        Product.objects.create(
            category=category,
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            image=image
        )
        return redirect("view_products")

    return render(request, "add_product.html", {"categories": categories})


def view_products(request):
    products = Product.objects.select_related("category").all()
    return render(request, "view_products.html", {"products": products})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        product.category = get_object_or_404(Category, id=category_id)

        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.quantity = request.POST.get("quantity")
        product.price = request.POST.get("price")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        return redirect("view_products")

    return render(request, "edit_product.html", {
        "product": product,
        "categories": categories
    })


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("view_products")



from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

# 📘 Add Book
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        description = request.POST.get("description")
        category = request.POST.get("category")
        publisher = request.POST.get("publisher")
        publication_date = request.POST.get("publication_date")
        cover_image = request.FILES.get("cover_image")

        Book.objects.create(
            title=title,
            author=author,
            description=description,
            category=category,
            publisher=publisher,
            publication_date=publication_date if publication_date else None,
            cover_image=cover_image
        )
        return redirect("view_books")
    return render(request, "add_book.html")


# 📚 List Books
def view_books(request):
    books = Book.objects.all().order_by("created_at")
    return render(request, "view_books.html", {"books": books})


# ✏️ Edit Book
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.description = request.POST.get("description")
        book.category = request.POST.get("category")
        book.publisher = request.POST.get("publisher")
        book.publication_date = request.POST.get("publication_date")
        if request.FILES.get("cover_image"):
            book.cover_image = request.FILES.get("cover_image")
        book.save()
        return redirect("view_books")
    return render(request, "edit_book.html", {"book": book})


# 🗑️ Delete Book
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("view_books")




from django.shortcuts import render
from userapp.models import ProductBooking, CartPayment, Cart

def admin_view_orders(request):
    # Single product bookings
    single_orders = ProductBooking.objects.select_related('product', 'category', 'user').all().order_by('-booking_date')

    # Cart order payments + items
    cart_payments = CartPayment.objects.select_related('user').all().order_by('-created_at')

    # Combine cart payments with their items
    cart_orders = []
    for pay in cart_payments:
        items = Cart.objects.filter(id__in=pay.cart_ids).select_related('product', 'category')
        cart_orders.append({
            "payment": pay,
            "items": items
        })

    return render(request, "admin_view_orders.html", {
        "single_orders": single_orders,
        "cart_orders": cart_orders
    })



from django.shortcuts import render, get_object_or_404
from userapp.models import ProductBooking, Cart, CartPayment

def admin_order_details(request, order_type, order_id):

    context = {}

    if order_type == "single":
        order = get_object_or_404(ProductBooking, id=order_id)

        context = {
            "type": "single",
            "order": order,
        }

    elif order_type == "cart":
        payment = get_object_or_404(CartPayment, id=order_id)
        cart_items = Cart.objects.filter(id__in=payment.cart_ids)

        context = {
            "type": "cart",
            "payment": payment,
            "items": cart_items,
        }

    return render(request, "admin_order_details.html", context)


from django.shortcuts import render
from userapp.models import tbl_register

def admin_view_users(request):
    users = tbl_register.objects.all().order_by('-id')   # latest first
    return render(request, "admin_view_users.html", {"users": users})