# Generated by Django 3.2 on 2024-11-10 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0002_prestamo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='libros/'),
        ),
    ]