# Generated by Django 3.2.16 on 2022-12-13 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=54, verbose_name='item')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('image', models.URLField(verbose_name='image')),
            ],
        ),
    ]