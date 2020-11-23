# Generated by Django 3.0.7 on 2020-06-23 02:10

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('visible', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Kit Categories',
            },
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('photo_1', models.ImageField(upload_to='kits/photos/%Y/%m/%d', verbose_name='Main Photo')),
                ('photo_2', models.ImageField(blank=True, null=True, upload_to='kits/photos/%Y/%m/%d')),
                ('photo_3', models.ImageField(blank=True, null=True, upload_to='kits/photos/%Y/%m/%d')),
                ('photo_4', models.ImageField(blank=True, null=True, upload_to='kits/photos/%Y/%m/%d')),
                ('photo_5', models.ImageField(blank=True, null=True, upload_to='kits/photos/%Y/%m/%d')),
                ('products', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_member_stock', models.IntegerField(default=50)),
                ('available', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(max_length=1000)),
                ('video_url', models.URLField(help_text='Youtube embeded url of an unlisted video', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VideoClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155)),
                ('photo', models.ImageField(upload_to='kits/classes/photos/%Y/%m/%d')),
                ('description', models.TextField(max_length=1000)),
                ('visible', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, default=10, help_text='In Euros (€)', max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'video classes',
            },
        ),
        migrations.CreateModel(
            name='VideoClassSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=False)),
                ('videos', models.ManyToManyField(to='subscription.Video')),
            ],
        ),
    ]