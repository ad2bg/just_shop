# Generated by Django 2.1.5 on 2019-02-07 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_cart_user'),
        ('users', '0003_remove_usermodel_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='cart',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='shop.Cart'),
        ),
    ]
