from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(
        default=0
    )  # for Dollar use models.DecimalFields
    active = models.BooleanField(default=True)
    image = models.ImageField(verbose_name=_("Product Image"), upload_to="product/product_image/", blank=True, )





    datetime_created = models.DateTimeField(auto_now_add=True)
    dateTime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk])


class ActiveCommentsManager:
    def get_queryset(self):
        return super(ActiveCommentsManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ("1", "Very Bad"),
        ("2", "Bad"),
        ("3", "Normal"),
        ("4", "Good"),
        ("5", "Perfect"),
    ]
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField(verbose_name=_("text"))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_("score"))

    datetime_created = models.DateTimeField(auto_now_add=True)
    dateTime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    # Manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManager()

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.product.id])
