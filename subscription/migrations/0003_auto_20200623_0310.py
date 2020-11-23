# Generated by Django 3.0.7 on 2020-06-23 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        ('subscription', '0002_videoclass_main_subscription_plan'),
        ('profiles', '0002_auto_20200623_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoclass',
            name='reviews',
            field=models.ManyToManyField(blank=True, to='profiles.Review'),
        ),
        migrations.AddField(
            model_name='videoclass',
            name='sections',
            field=models.ManyToManyField(to='subscription.VideoClassSection'),
        ),
        migrations.AddField(
            model_name='videoclass',
            name='subscription_plans',
            field=models.ManyToManyField(blank=True, related_name='subscription_plans', to='transactions.SubscriptionPlan'),
        ),
        migrations.AddField(
            model_name='video',
            name='comments',
            field=models.ManyToManyField(blank=True, to='profiles.Comment'),
        ),
        migrations.AddField(
            model_name='kit',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.Category'),
        ),
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