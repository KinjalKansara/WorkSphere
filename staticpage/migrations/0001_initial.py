# Generated by Django 5.0.6 on 2025-02-02 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=255)),
                ('last', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
