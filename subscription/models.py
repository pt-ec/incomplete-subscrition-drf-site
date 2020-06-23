from django.db import models
from django.contrib.auth import get_user_model
from django_better_admin_arrayfield.models.fields import ArrayField

from profiles.models import Review, Comment
from transactions.models import SubscriptionPlan
User = get_user_model()


class Category(models.Model):
    """ Kit Category model """
    title = models.CharField(max_length=200, unique=True)
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Kit Categories'


class Kit(models.Model):
    """ Kit model """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
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


class Video(models.Model):
    """ Youtube video for Kit class """
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=1000)
    video_url = models.URLField(
        unique=True, help_text='Youtube embeded url of an unlisted video')
    comments = models.ManyToManyField(Comment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VideoClassSection(models.Model):
    """ Video Class Section model """
    name = models.CharField(max_length=300)
    videos = models.ManyToManyField(Video)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VideoClass(models.Model):
    """ Kit Category Video Class  """
    title = models.CharField(max_length=155)
    main_subscription_plan = models.ForeignKey(SubscriptionPlan,
                                               on_delete=models.CASCADE)
    subscription_plans = models.ManyToManyField(
        SubscriptionPlan, blank=True, related_name='subscription_plans')
    photo = models.ImageField(upload_to='kits/classes/photos/%Y/%m/%d')
    description = models.TextField(max_length=1000)
    sections = models.ManyToManyField(VideoClassSection)
    reviews = models.ManyToManyField(Review, blank=True)
    visible = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=14, decimal_places=2, default=10, help_text='In Euros (€)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'video classes'

    def __str__(self):
        return self.title
