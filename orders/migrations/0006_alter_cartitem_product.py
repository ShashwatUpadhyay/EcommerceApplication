# Generated by Django 5.1.7 on 2025-03-24 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order'),
        ('shop', '0009_alter_product_min_order_quanitity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incart', to='shop.product'),
        ),
    ]
