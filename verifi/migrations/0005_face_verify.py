# Generated by Django 4.1 on 2023-12-15 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verifi", "0004_remove_result_recogontions_result_recognition_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="face",
            name="verify",
            field=models.BooleanField(default=False),
        ),
    ]
