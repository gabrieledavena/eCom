# Generated by Django 5.1.2 on 2024-11-26 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0013_remove_prodotto_marca"),
    ]

    operations = [
        migrations.AddField(
            model_name="prodotto",
            name="marca",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="store.marca"
            ),
        ),
    ]
