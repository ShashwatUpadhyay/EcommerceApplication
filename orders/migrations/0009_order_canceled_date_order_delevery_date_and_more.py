# Generated by Django 5.1.7 on 2025-03-25 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='canceled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delevery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='refunded_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='returned_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
