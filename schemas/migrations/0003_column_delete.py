# Generated by Django 4.1.7 on 2023-03-12 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0002_alter_column_schema_alter_schema_column_characters_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='DELETE',
            field=models.BooleanField(default=False),
        ),
    ]