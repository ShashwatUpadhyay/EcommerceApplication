# Generated by Django 5.1.7 on 2025-04-05 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_remove_whislist_added_at_alter_whislist_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.FloatField(default=0.0, verbose_name='Tax %'),
        ),
    ]
