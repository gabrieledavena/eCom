# Generated by Django 5.1.2 on 2024-10-12 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_alter_customer_cognome_alter_customer_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="indirizzo",
            field=models.CharField(default="", max_length=50),
        ),
    ]
