from django.db import models
from profiles.models import Comment, Review
from transactions.models import SubscriptionPlan


class Video(models.Model):
    """ Youtube video for Kit class """
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(unique=True)
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
    title = models.CharField(max_length=155, unique=True)
    main_subscription_plan = models.ForeignKey(SubscriptionPlan,
                                               on_delete=models.CASCADE)
    subscription_plans = models.ManyToManyField(
        SubscriptionPlan, blank=True, related_name='subscription_plans')
    slug = models.SlugField(unique=True)
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
