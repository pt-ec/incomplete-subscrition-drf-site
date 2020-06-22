from datetime import date

from django.db import models

from profiles.models import Comment


class BlogPost(models.Model):
    """ Blog post model """
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True,
                            help_text="This is pre-populated by the title")
    author = models.CharField(max_length=100, default='Conceição Cabral')
    body = models.TextField(max_length=1000, blank=True, null=True)
    photo_1 = models.ImageField(upload_to='blog/photos/%Y/%m/%d',
                                verbose_name='Main Photo')
    photo_2 = models.ImageField(
        upload_to='blog/photos/%Y/%m/%d', blank=True, null=True)
    photo_3 = models.ImageField(
        upload_to='blog/photos/%Y/%m/%d', blank=True, null=True)
    written_at = models.DateField(default=date.today)
    comments = models.ManyToManyField(Comment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        """ Return string representation of blog post """
        return f'{self.title} by {self.author}'
