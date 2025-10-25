from django.db import models




# Product
# name
# description
# price
# add date and time
class Product(models.Model):
    name = models.CharField(max_length=255)
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
    ORDER_STATUS_PAID = 'P'
    ORDER_STATUS_UNPAID = 'U'
    ORDER_STATUS_CANCELED = 'C'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID ,'Paid'),
        (ORDER_STATUS_UNPAID ,'Unpaid'),
        (ORDER_STATUS_CANCELED ,'Canceled'),
    ]
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='u')

# Comment
# name
# body
# date of creation
# status { Waiting OR Aproved OR Not_Aproved}
class Comment(models.Model):
    # product => Foreign Key
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APROVED = 'a'
    COMMENT_STATUS_NOT_APROCED = 'n'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING,'waiting'),
        (COMMENT_STATUS_APROVED,'aproved'),
        (COMMENT_STATUS_NOT_APROCED,'not aproved'),
    ]
    name = ""
    body = models.TextField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=COMMENT_STATUS, default='w')





