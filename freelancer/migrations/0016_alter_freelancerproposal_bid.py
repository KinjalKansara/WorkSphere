# Generated by Django 5.0.6 on 2025-01-19 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0015_alter_freelancerproposal_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancerproposal',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
