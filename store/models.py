from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    detetime_created = models.DateTimeField(auto_now_add=True)

# Product
# name
# description
# price
# add date and time
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField(default=0)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

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


class Order(models.Model):
    # customer => Foreign Key
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
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

# Comment
# name
# body
# date of creation
# status { Waiting OR Aproved OR Not_Aproved}
class Comment(models.Model):
    # product => Foreign Key
    # One Many
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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





