from django.db import models


class Product(models.Model):
    item = models.CharField(max_length=54, verbose_name='item')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    image = models.CharField(max_length=54, verbose_name='image')
    description = models.TextField(verbose_name='description')

    def __str__(self):
        return str(self.item) + ": $" + str(self.price)


class Cart(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='products')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ": $" + str(self.price) + ": $" + str(self.date)
