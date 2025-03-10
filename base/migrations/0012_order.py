# Generated by Django 4.2.16 on 2024-11-08 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_rename_userinfo_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.CharField(max_length=200, unique=True)),
                ('totalPrice', models.FloatField()),
                ('status', models.CharField(choices=[('Order placed', 'Order placed'), ('Order cancelled', 'Order cancelled'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.usersignup')),
                ('items', models.ManyToManyField(to='base.fooditem')),
            ],
        ),
    ]
