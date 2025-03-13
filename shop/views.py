from django.shortcuts import render
from .models import Product, Category

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'products': products , 'categories': categories})

def category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category_products.html', {'products': products , 'categories': categories})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})