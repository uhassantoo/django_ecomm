from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category , Cart , CartItem , Order , OrderItem 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'products': products , 'categories': categories})

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'shop/category_products.html', {'products': products , 'categories': categories , 'category': category})

@login_required
def cart_detail(request):
    cart , created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items , 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart , created = Cart.objects.get_or_create(user=request.user)
    cart_item , created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return redirect('cart_detail')
    order = Order.objects.create(user=request.user, total_price=0)
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        item.delete()
    order.total_price = total_price
    order.save()
    cart_items.delete()

@login_required
def order_summary(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_summary.html', {'orders': orders})   

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_detail.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})