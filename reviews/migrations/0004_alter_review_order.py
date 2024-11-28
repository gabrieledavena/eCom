# Generated by Django 5.1.2 on 2024-11-28 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0005_order_shipped_at"),
        ("reviews", "0003_alter_review_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="checkout.order",
            ),
        ),
    ]
