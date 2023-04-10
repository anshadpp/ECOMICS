from django.db import models
from django.contrib.auth.models import User




CATEGORY_CHOICES=(
    ('AC','Action'),
    ('CM','Comedy'),
    ('DR','Drama')
)



class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image =models.ImageField(upload_to='product')
    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    pincode = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return self.product.discounted_price



class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    @property
    def total_cost(self):
        return self.product.discounted_price

