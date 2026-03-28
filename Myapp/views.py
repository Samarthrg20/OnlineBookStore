from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, Order


# 📖 View Books (with search)
def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'book_list.html', {'books': books})


# 👤 Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if username exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')


# 🔐 Login
def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('book_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# 🚪 Logout
def user_logout(request):
    logout(request)
    return redirect('login')


# 🛒 Add to Cart
@login_required
def add_to_cart(request, id):
    book = get_object_or_404(Book, id=id)

    # Prevent duplicate items
    if not Cart.objects.filter(user=request.user, book=book).exists():
        Cart.objects.create(user=request.user, book=book)

    return redirect('cart')


# 🛒 View Cart
@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'items': items})


# ❌ Remove from Cart (DELETE)
@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Cart, id=id)
    item.delete()
    return redirect('cart')


# ✅ Place Order (with confirmation page)
@login_required
def place_order(request, id):
    item = get_object_or_404(Cart, id=id)

    if request.method == 'POST':
        Order.objects.create(user=request.user, book=item.book)
        item.delete()
        return redirect('cart')

    return render(request, 'order.html', {'item': item})