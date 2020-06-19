# Generated by Django 3.0.7 on 2020-06-18 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0002_auto_20200615_1807'),
        ('profiles', '0003_auto_20200617_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=1000)),
                ('video_url', models.URLField(help_text='Youtube embeded url of an unlisted video', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=False)),
                ('comments', models.ManyToManyField(blank=True, to='profiles.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='VideoClassSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=False)),
                ('videos', models.ManyToManyField(to='subscription_classes.Video')),
            ],
        ),
        migrations.CreateModel(
            name='VideoClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('photo', models.ImageField(upload_to='kits/classes/photos/%Y/%m/%d')),
                ('description', models.TextField(max_length=1000)),
                ('visible', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reviews', models.ManyToManyField(blank=True, to='profiles.Review')),
                ('sections', models.ManyToManyField(to='subscription_classes.VideoClassSection')),
                ('subscription_plans', models.ManyToManyField(blank=True, related_name='Kit', to='transactions.SubscriptionPlan')),
            ],
            options={
                'verbose_name_plural': 'video classes',
            },
        ),
    ]
