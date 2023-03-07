from amado.models import Comments, Product, ProductImage, CommentImage
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'item',
            'price',
            'description',
        )


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = (
            'product_pk',
            'images',
        )


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('title', 'text', 'rating')


class CommentImageForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'



