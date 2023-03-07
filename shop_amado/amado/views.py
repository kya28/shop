from collections import OrderedDict
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from amado.models import Product, Cart, Order, Comments, ProductImage, CommentImage
from amado.forms import CommentsForm, CommentImageForm, ProductImageForm, ProductForm


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
    product_image = ProductImage.objects.all().distinct('product_pk')

    return render(request, 'amado/index.html', {'products': productss, 'product_image': product_image})


def product_detail(request, product_pk):
    if request.method == 'POST':
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            product = Product.objects.get(pk=product_pk)
            comment = comments_form.save(commit=False)
            comment.user = request.user
            comment.product_pk = product
            comment.save()
            # comments_form.clear()
            return redirect('product_detail', product_pk)
    else:
        comments_form = CommentsForm()
        comments = Comments.objects.filter(product_pk=product_pk)
        product = get_object_or_404(Product, pk=product_pk)
        paginator = Paginator(comments, 1)
        page = request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        product_image = ProductImage.objects.all().distinct('product_pk')
        return render(request, 'amado/product-details.html',
                      {'product': product,
                       'comments': comments,
                       'comments_form': comments_form,
                       'page': page,
                       'product_image': product_image})


def shop(request):
    products = Product.objects.all()
    product_image = ProductImage.objects.all().distinct('product_pk')
    return render(request, 'amado/shop.html', {'products': products, 'product_image': product_image})


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
    product_image = ProductImage.objects.all().distinct("product_pk")
    return render(request, 'amado/cart.html', {'cart': cart_all.products.all(), 'quantity': quantity,
                                               'cart_total': cart_total, 'product_image': product_image})


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


# def comments(request, pk_product):
#     if request.method == 'POST':
#         comments_form = CommentsForm()
#         if comments_form.is_valid():
#             comments_form.save(user=request.user)
#     comments = Comments.objects.filter(pk=pk_product)
#     return render(request, 'amado/product-details.html', {'comments': comments, 'comments_form': comments_form})


def product_all(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        product_image_form = ProductImageForm(request.POST, files=request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.save()
            image = product_image_form.save(commit=False)
            image.save()
            return redirect('index')
        else:
            return HttpResponse("There was an error with your submission.Please try again.")
    else:
        product_form = ProductForm()
        product_image_form = ProductImageForm()
        products = Product.objects.all()
        return render(request, 'amado/product_all.html', {'products': products, 'product_form': product_form,
                                                          'product_image_form': product_image_form})
