# Generated by Django 5.2 on 2025-04-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
