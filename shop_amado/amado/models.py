from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    item = models.CharField(max_length=54, verbose_name='item')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    description = models.TextField(verbose_name='description')

    def __str__(self):
        return str(self.item) + ": $" + str(self.price)


class ProductImage(models.Model):
    product_pk = models.ForeignKey('Product', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='static/amado/img/product', null=True, blank=True)


class Cart(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='products')

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ": $" + str(self.price) + ": $" + str(self.date)


class Comments(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product_pk = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    #image = models.ImageField(upload_to='static/amado/img/comment', null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.user) + ": $" + str(self.product_pk) + ": $" + str(self.title)


class CommentImage(models.Model):
    comment_pk = models.ForeignKey('Comments', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='static/amado/img/comment', null=True, blank=True)