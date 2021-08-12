from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    user_mobile = models.IntegerField(null=True)
    user_address = models.TextField(verbose_name='Address', blank=True, null=True)
    user_image = models.ImageField(blank=True, null=True, upload_to='profileimages/', )
    is_hospital_staff = models.BooleanField(verbose_name="Hospital Staff", default=False, )
    is_patient = models.BooleanField(verbose_name="Patient", default=False, )
    is_doctor = models.BooleanField(verbose_name="Doctor", default=False, )
    objects = UserManager()

    class Meta:
        verbose_name_plural = '1. Users'

    def __str__(self):
        return self.username


class Blogs(models.Model):
    blog_title = models.CharField(verbose_name='Title', max_length=255)
    blog_slug = models.SlugField(verbose_name='Slug', max_length=255)
    blog_desc = models.TextField(verbose_name='Description', max_length=20000)
    blog_pubdate = models.DateTimeField(verbose_name='Published Date & Time', default=datetime.now, blank=True,
                                        null=True)
    blog_publish = models.BooleanField(verbose_name="Publish Status")
    blog_img = models.ImageField(verbose_name='Image', upload_to='blogimages/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Articles'
        verbose_name = "Articles"

    def __str__(self):
        return self.blog_title


class Appointments(models.Model):
    a_status_ch = (
        ('1', 'Pending'),
        ('2', 'Canceled'),
        ('3', 'Confirm'),
        ('4', 'Complete'),
    )
    patient = models.ForeignKey(User, models.SET_NULL, verbose_name='Patient',
                                blank=True, null=True, related_name="patient", limit_choices_to={'is_patient': True}, )
    p_h_problem = models.TextField(verbose_name='Health Problem', blank=True, null=True)
    doctor = models.ForeignKey(User, models.SET_NULL, verbose_name='Doctor',
                               blank=True, null=True, related_name="doctor", limit_choices_to={'is_doctor': True})
    a_status = models.CharField(verbose_name='Appointment Status', max_length=20, choices=a_status_ch,
                                default='1', blank=True, null=True)
    a_date_time = models.DateTimeField(verbose_name='Date And Time', blank=True, null=True)
    a_meeting_id = models.CharField(verbose_name='Appointment Meeting ID', max_length=255, blank=True, null=True)
    checkup_report = models.TextField(verbose_name='Report', blank=True, null=True)
    checkup_report_file = models.FileField(verbose_name='Report File', upload_to='checkupreport/', blank=True,
                                           null=True)
    d_prescription = models.TextField(verbose_name='Doctor Prescription', blank=True, null=True)


class PtoSNotification(models.Model):
    appointment_id = models.IntegerField(verbose_name="Appointment id")
    patient = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Patient to Staff Notification'

    def __str__(self):
        return str(self.id)


class StoPNotification(models.Model):
    appointment_id = models.IntegerField(verbose_name="Appointment id")
    patient = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Staff to Patient Notification'

    def __str__(self):
        return str(self.id)


class StoDNotification(models.Model):
    appointment_id = models.IntegerField(verbose_name="Appointment id")
    doctor = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Staff to Doctor Notification'

    def __str__(self):
        return str(self.id)


class DtoPNotification(models.Model):
    appointment_id = models.IntegerField(verbose_name="Appointment id")
    doctor = models.CharField(max_length=255)
    patient = models.CharField(max_length=255)
    meeting_id = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Doctor to Patient Notification'

    def __str__(self):
        return str(self.id)
