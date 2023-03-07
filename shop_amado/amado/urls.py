from django.conf.urls.static import static
from django.urls import path, include
from amado.views import index, shop, product_detail, cart, cart_add, cart_delete_product, cart_all_delete, \
    order, user_order, popular_products, product_all

from shop_amado import settings

urlpatterns = [
    path('', index, name='index'),
    path('shop', shop, name='shop'),
    path('product_detail/<int:product_pk>', product_detail, name='product_detail'),
    path('shop/cart', cart, name='cart'),
    path('product_detail/cart_add/<int:product_pk>', cart_add, name='cart_add'),
    path('cart/cart_delete_product/<int:product_pk>', cart_delete_product, name='cart_delete_product'),
    path('cart/cart_all_delete', cart_all_delete, name='cart_all_delete'),
    path('orders', order, name='order'),
    path('user_orders', user_order, name='user_order'),
    path('shop/popular_products', popular_products, name='popular_products'),
    path('shop/product_all', product_all, name='product_all')


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
