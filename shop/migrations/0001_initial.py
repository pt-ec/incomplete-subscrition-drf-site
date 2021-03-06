# Generated by Django 3.0.7 on 2020-06-23 02:10

from django.db import migrations, models
import django.db.models.deletion
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
                ('title', models.CharField(max_length=150, unique=True)),
                ('visible', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('T', 'Bank Transfer'), ('B', 'Card or Paypal Payment')], max_length=1)),
                ('payed', models.BooleanField(default=False)),
                ('shipped', models.BooleanField(default=False)),
                ('shipped_date', models.DateTimeField(blank=True, null=True)),
                ('received', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('visible', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'subcategories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('photo_1', models.ImageField(upload_to='products/photos/%Y/%m/%d', verbose_name='Main Photo')),
                ('photo_2', models.ImageField(blank=True, null=True, upload_to='products/photos/%Y/%m/%d')),
                ('photo_3', models.ImageField(blank=True, null=True, upload_to='products/photos/%Y/%m/%d')),
                ('photo_4', models.ImageField(blank=True, null=True, upload_to='products/photos/%Y/%m/%d')),
                ('photo_5', models.ImageField(blank=True, null=True, upload_to='products/photos/%Y/%m/%d')),
                ('description', models.TextField(max_length=1000)),
                ('stock', models.IntegerField(default=1)),
                ('unique', models.BooleanField(default=True)),
                ('available', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, default=10, help_text='In Euros (€)', max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('materials', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=60), size=None)),
                ('length', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('length_unit', models.CharField(blank=True, choices=[('', 'Select Unit'), ('m', 'Meter'), ('dm', 'Decimeter'), ('cm', 'Centimeter'), ('mm', 'Millimeter'), ('in', 'Inches')], default='', max_length=2)),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('width_unit', models.CharField(blank=True, choices=[('', 'Select Unit'), ('m', 'Meter'), ('dm', 'Decimeter'), ('cm', 'Centimeter'), ('mm', 'Millimeter'), ('in', 'Inches')], default='', max_length=2)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('height_unit', models.CharField(blank=True, choices=[('', 'Select Unit'), ('m', 'Meter'), ('dm', 'Decimeter'), ('cm', 'Centimeter'), ('mm', 'Millimeter'), ('in', 'Inches')], default='', max_length=2)),
                ('diameter', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('diameter_unit', models.CharField(blank=True, choices=[('', 'Select Unit'), ('m', 'Meter'), ('dm', 'Decimeter'), ('cm', 'Centimeter'), ('mm', 'Millimeter'), ('in', 'Inches')], default='', max_length=2)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=9)),
                ('weight_unit', models.CharField(choices=[('kg', 'Kilogram'), ('g', 'Gram'), ('lb', 'Pound')], default='kg', max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('purchased', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
        ),
    ]
