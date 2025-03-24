from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

# Register Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

# Register Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock']
    search_fields = ['name']
    list_filter = ['category', 'price']

admin.site.register(Product, ProductAdmin)

# Register other models
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
