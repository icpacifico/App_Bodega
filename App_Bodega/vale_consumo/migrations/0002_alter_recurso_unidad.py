# Generated by Django 4.2 on 2023-08-28 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vale_consumo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurso',
            name='unidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vale_consumo.unidade'),
        ),
    ]
