# Generated by Django 5.0.4 on 2024-04-10 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_customuser_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name_plural': 'CustomUser'},
        ),
    ]
