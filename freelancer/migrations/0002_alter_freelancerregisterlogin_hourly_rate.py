# Generated by Django 5.0.6 on 2025-01-23 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancerregisterlogin',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
