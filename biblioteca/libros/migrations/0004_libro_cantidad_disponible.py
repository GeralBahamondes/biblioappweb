# Generated by Django 3.2 on 2024-11-10 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0003_libro_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='cantidad_disponible',
            field=models.PositiveIntegerField(default=1),
        ),
    ]