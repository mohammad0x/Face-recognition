# Generated by Django 4.1 on 2023-12-12 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verifi", "0002_alter_face_point"),
    ]

    operations = [
        migrations.AlterField(
            model_name="face",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="face",
            name="point",
            field=models.TextField(),
        ),
    ]