# Generated by Django 4.2 on 2023-04-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vale_consumo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='observacion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Observacion',
        ),
    ]
