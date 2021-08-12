# Generated by Django 3.2 on 2021-04-27 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210426_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_h_problem', models.TextField(blank=True, null=True, verbose_name='Health Problem')),
                ('a_status', models.CharField(blank=True, choices=[('1', 'Pending'), ('2', 'Canceled'), ('3', 'Confirm'), ('4', 'Complete')], default='1', max_length=20, null=True, verbose_name='Appointment Status')),
                ('a_date_time', models.DateTimeField(blank=True, null=True, verbose_name='sign time')),
                ('a_meeting_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Appointment Meeting ID')),
                ('checkup_report', models.TextField(blank=True, null=True, verbose_name='Report')),
                ('checkup_report_file', models.FileField(blank=True, null=True, upload_to='checkupreport/', verbose_name='Report File')),
                ('d_prescription', models.TextField(blank=True, null=True, verbose_name='Report')),
                ('doctor', models.ForeignKey(blank=True, limit_choices_to={'is_doctor': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor', to=settings.AUTH_USER_MODEL, verbose_name='Doctor')),
                ('patient', models.ForeignKey(blank=True, limit_choices_to={'is_patient': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient', to=settings.AUTH_USER_MODEL, verbose_name='Patient')),
            ],
        ),
    ]
