# Generated by Django 4.2 on 2023-08-28 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vale_consumo', '0002_alter_recurso_unidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='retira',
            field=models.CharField(max_length=10),
        ),
    ]
