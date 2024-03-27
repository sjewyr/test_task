# Generated by Django 5.0.3 on 2024-03-27 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("personapi", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mailbox",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mailboxes",
                        to="personapi.person",
                    ),
                ),
            ],
        ),
    ]