# Generated by Django 3.2 on 2023-06-19 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Ingredient name')),
                ('measurement_unit', models.CharField(max_length=32, verbose_name='Measurement unit')),
            ],
        ),
    ]
