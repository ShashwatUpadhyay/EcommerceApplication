# Generated by Django 5.1.7 on 2025-03-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_product_min_quanitity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='min_order_quanitity',
            field=models.PositiveIntegerField(default=1, verbose_name='Minimum order queantity'),
        ),
    ]
