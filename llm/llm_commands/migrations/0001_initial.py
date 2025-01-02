# Generated by Django 5.1.4 on 2025-01-01 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_title', models.CharField(max_length=255)),
                ('city_name', models.CharField(max_length=255)),
                ('hotel_id', models.CharField(max_length=255, unique=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('rating', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('room_type', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hotels',
            },
        ),
        migrations.CreateModel(
            name='PropertyRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('review', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='llm_commands.hotel')),
            ],
            options={
                'db_table': 'property_ratings',
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summaries', to='llm_commands.hotel')),
            ],
            options={
                'db_table': 'property_summaries',
            },
        ),
    ]