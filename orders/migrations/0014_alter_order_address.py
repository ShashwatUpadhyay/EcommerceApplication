# Generated by Django 5.1.7 on 2025-03-26 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_userextra_change_password_token'),
        ('orders', '0013_alter_order_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.address'),
        ),
    ]
