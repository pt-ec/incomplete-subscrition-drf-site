# Generated by Django 3.0.7 on 2020-06-23 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoclass',
            name='main_subscription_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.SubscriptionPlan'),
        ),
    ]
