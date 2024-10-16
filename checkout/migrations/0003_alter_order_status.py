# Generated by Django 5.1.2 on 2024-10-16 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0002_order_orderitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("ACCEPTED", "Accepted"),
                    ("COMPLETED", "Completed"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
