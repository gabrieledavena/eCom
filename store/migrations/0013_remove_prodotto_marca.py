# Generated by Django 5.1.2 on 2024-11-26 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_marca_prodotto_marca"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="prodotto",
            name="marca",
        ),
    ]