# Generated by Django 4.1 on 2023-12-24 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verifi", "0006_face_noise"),
    ]

    operations = [
        migrations.AlterField(
            model_name="face",
            name="point",
            field=models.TextField(null=True),
        ),
    ]
