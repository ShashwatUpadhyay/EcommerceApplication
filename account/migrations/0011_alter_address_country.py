# Generated by Django 5.1.7 on 2025-03-24 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_address_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
