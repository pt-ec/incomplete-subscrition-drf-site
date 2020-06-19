from datetime import datetime
# From Django
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django_better_admin_arrayfield.models.fields import ArrayField

from profiles.models import Review
from transactions.models import SubscriptionPlan
from api_project.extras import schengen_area
User = get_user_model()


class Category(models.Model):
    """ Kit Category model """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Kit(models.Model):
    """ Kit model """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=1000)
    photo_1 = models.ImageField(upload_to='kits/photos/%Y/%m/%d',
                                verbose_name='Main Photo')
    photo_2 = models.ImageField(upload_to='kits/photos/%Y/%m/%d',
                                blank=True, null=True)
    photo_3 = models.ImageField(upload_to='kits/photos/%Y/%m/%d',
                                blank=True, null=True)
    photo_4 = models.ImageField(upload_to='kits/photos/%Y/%m/%d',
                                blank=True, null=True)
    photo_5 = models.ImageField(upload_to='kits/photos/%Y/%m/%d',
                                blank=True, null=True)
    products = ArrayField(models.CharField(max_length=200))
    subscription_plan = models.ForeignKey(SubscriptionPlan,
                                          on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    new_member_stock = models.IntegerField(default=50)
    available = models.BooleanField(default=False)
    reviews = models.ManyToManyField(Review)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
