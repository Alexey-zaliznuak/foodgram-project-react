# Generated by Django 3.2 on 2023-07-01 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',), 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]