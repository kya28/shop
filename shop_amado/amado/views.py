from collections import OrderedDict

from django.shortcuts import render, get_object_or_404, redirect

from amado.models import Product, Cart, Order


def popular_products():
    products = Product.objects.all()
    pop_products = {}
    for product in products:
        pop_products[product.item] = product.orders.all().count()
    p = dict(sorted(pop_products.items(), key=lambda x: -x[1]))
    return p


def product_quantity_add(request, product_pk):
    cart_user = Cart.objects.filter(user=request.user).first()
    products = cart_user.products.all()
    product = products.filter(pk=product_pk).first()
    return redirect('cart')


def index(request):
    p = popular_products()
    productss = []
    for i in p:
        product = Product.objects.filter(item=i).first()
        productss.append(product)
    return render(request, 'amado/index.html', {'products': productss})


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    return render(request, 'amado/product-details.html', {'product': product})


def shop(request):
    products = Product.objects.all()
    return render(request, 'amado/shop.html', {'products': products})


def cart_add(request, product_pk):
    product = Product.objects.filter(pk=product_pk).first()
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None:
        cart = Cart.objects.create(user=request.user)
    cart.products.add(product)
    return redirect('product_detail', product_pk=product.pk)


def cart(request):
    cart_all = Cart.objects.filter(user=request.user).first()
    quantity = cart_all.products.all().count()
    products = cart_all.products.all()
    cart_total = sum([i.price for i in products])
    return render(request, 'amado/cart.html', {'cart': cart_all.products.all(), 'quantity': quantity,
                                               'cart_total': cart_total})


def cart_delete_product(request, product_pk):
    cart_delete = Cart.objects.filter(user=request.user).first()
    cart_delete.products.remove(product_pk)
    return redirect('cart')


def cart_all_delete(request):
    cart_delete = Cart.objects.filter(user=request.user).first()
    cart_delete.products.clear()
    return redirect('cart')


def user_order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'amado/order.html', {'orders': orders})


def order(request):
    cart = Cart.objects.filter(user=request.user).first()
    products = cart.products.all()
    cart_total = sum([i.price for i in products])
    order = Order.objects.create(user=request.user, price=cart_total)
    order.products.add(*products)
    cart.products.clear()
    return redirect('user_order')
