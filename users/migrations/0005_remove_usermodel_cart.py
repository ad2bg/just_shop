# Generated by Django 2.1.5 on 2019-02-07 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_usermodel_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='cart',
        ),
    ]