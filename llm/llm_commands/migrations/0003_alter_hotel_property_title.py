# Generated by Django 5.1.4 on 2025-01-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm_commands', '0002_alter_propertyrating_table_alter_summary_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='property_title',
            field=models.CharField(default='Untitled Hotel', max_length=255),
        ),
    ]
