from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    detetime_created = models.DateTimeField(auto_now_add=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)



class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

# Product
# name
# description
# price
# add date and time
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField(default=0)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(Discount, blank=True, related_name='products')

# Customer:
#   first_name
#   last_name
#   email
#   phone_number
#   birth_date
class Customer(models.Model):
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

# Order
# Who has created this order and when ?
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    ORDER_STATUS_PAID = 'P'
    ORDER_STATUS_UNPAID = 'U'
    ORDER_STATUS_CANCELED = 'C'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID ,'Paid'),
        (ORDER_STATUS_UNPAID ,'Unpaid'),
        (ORDER_STATUS_CANCELED ,'Canceled'),
    ]
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)


# OrderItem
# what product ? - quantity ? - for what order ?
#   product => Foreign_Key
#   quantity
#   Order -> Foreign Key
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = [['order', 'product']]

# Cart
# When this cart is created ?
#   datetime_created 
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)



# CartItem
# What product ? - quantity ? - for what cart ?
#   Cart -> foreign_key
#   product => Foreign_Key
#   quantity
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]



# Comment
# name
# body
# date of creation
# status { Waiting OR Aproved OR Not_Aproved}
class Comment(models.Model):
    # product => Foreign Key
    # One Many
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APROVED = 'a'
    COMMENT_STATUS_NOT_APROCED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING,'Waiting'),
        (COMMENT_STATUS_APROVED,'Approved'),
        (COMMENT_STATUS_NOT_APROCED,'Not Approved'),
    ]
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_NOT_APROCED)








