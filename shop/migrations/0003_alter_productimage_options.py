# Generated by Django 5.1.7 on 2025-03-21 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'get_latest_by': 'created_at'},
        ),
    ]
