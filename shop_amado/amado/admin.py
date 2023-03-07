from django.contrib import admin
from amado.models import Product, Cart, Order, Comments, ProductImage, CommentImage

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Comments)
admin.site.register(CommentImage)

