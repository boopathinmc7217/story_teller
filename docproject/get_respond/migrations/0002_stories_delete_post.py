# Generated by Django 5.0 on 2023-12-29 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("get_respond", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stories",
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
            ],
        ),
        migrations.DeleteModel(
            name="Post",
        ),
    ]
