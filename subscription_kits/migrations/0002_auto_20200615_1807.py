# Generated by Django 3.0.7 on 2020-06-15 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscription_kits', '0001_initial'),
        ('transactions', '0001_initial'),
        ('profiles', '0002_auto_20200615_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='kit',
            name='reviews',
            field=models.ManyToManyField(to='profiles.Review'),
        ),
        migrations.AddField(
            model_name='kit',
            name='subscription_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.SubscriptionPlan'),
        ),
    ]