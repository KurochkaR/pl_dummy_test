# Generated by Django 4.1.7 on 2023-03-12 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0003_column_delete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='DELETE',
        ),
    ]