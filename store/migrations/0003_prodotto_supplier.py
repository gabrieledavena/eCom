# Generated by Django 5.1.2 on 2024-10-10 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
        ("store", "0002_alter_prodotto_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="prodotto",
            name="supplier",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.supplier",
            ),
        ),
    ]
