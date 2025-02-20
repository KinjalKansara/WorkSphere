# Generated by Django 5.0.6 on 2025-02-20 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreelancerRegisterLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ImageField(upload_to='profile_images/')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('skills', models.CharField(max_length=50)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=20)),
                ('location', models.CharField(max_length=100)),
                ('about_me', models.TextField(max_length=1000, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=50, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=20, null=True)),
                ('account_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FreelancerProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(editable=False)),
                ('duration', models.CharField(choices=[('1_day', '1 Day'), ('2_days', '2 Days'), ('3_days', '3 Days'), ('4_days', '4 Days'), ('5_days', '5 Days'), ('7_days', '7 Days'), ('10_days', '10 Days'), ('15_days', '15 Days'), ('1_month', '1 Month'), ('2_months', '2 Months'), ('3_months', '3 Months')], max_length=20)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cover_letter', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=10, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.clientregisterlogin')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.clientpostproject')),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancerregisterlogin')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid', max_length=20)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancerproposal')),
            ],
        ),
    ]
