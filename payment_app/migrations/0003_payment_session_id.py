# Generated by Django 5.0.2 on 2024-02-21 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0002_alter_payment_product_delete_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='session_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
