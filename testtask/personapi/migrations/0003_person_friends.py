# Generated by Django 5.0.3 on 2024-03-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("personapi", "0002_mailbox"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="friends",
            field=models.ManyToManyField(to="personapi.person"),
        ),
    ]
