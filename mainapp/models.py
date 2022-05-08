from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.utils.text import slugify


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


class Products(models.Model):
    product_img = models.ImageField(upload_to="productsimages/", blank=False)
    product_title = models.CharField(max_length=255, unique=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_desc = models.TextField()
    product_count = models.CharField(max_length=10)
    product_slug = models.SlugField(blank=True, null=True, unique=True)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product_slug = slugify(self.product_title)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_title


class ProductImage(models.Model):
    product = models.ForeignKey(Products, verbose_name='Product Title', default=None, on_delete=models.CASCADE)
    product_images = models.ImageField(verbose_name='Image', upload_to='productsimages/')

    class Meta:
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return self.product.product_title

class OrderProductInfo(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(Products, models.SET_NULL, blank=True, null=True)
    product_quantity = models.IntegerField()
    single_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_product_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.product_title


class CustomePaymentMethod(models.Model):
    made_on = models.DateTimeField(auto_now_add=True)
    upi_transaction_id = models.CharField(max_length=100)
    upi_id = models.CharField(max_length=200)
    payment_proof = models.FileField(upload_to="paymentproof/")

    def __str__(self):
        return str(self.id)


class CourierDetail(models.Model):
    start_delivery_date = models.DateTimeField()
    end_delivery_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    contact_no = models.BigIntegerField()
    contact_email = models.EmailField()
    tracking_id = models.CharField(max_length=200)



class Orders(models.Model):
    order_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    contry_choice = (('1', 'India'), ('2', 'USA'), ('3', 'Canada'), ('4', 'Bhutan'), ('5', 'Japan'))
    oderpayment_choice = (('1', 'Paytm'), ('2', 'Razorpay'), ('3', 'Custome'))
    orderstatus_choice = (('1', 'Placed'), ('2', 'Confirm'), ('3', 'Out for Delivery'), ('4', 'Complete'), ('5', 'Failed'))
    orderpaymentstatus_choice = (('1', 'Paid'), ('2', 'Pending'), ('3', 'Failed'))
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField()
    customer_contry = models.CharField(max_length=30, choices=contry_choice)
    customer_state = models.CharField(max_length=100)
    customer_city = models.CharField(max_length=100)
    city_zip = models.IntegerField()
    customer_email = models.EmailField()
    customer_mobile_number = models.BigIntegerField()
    products = models.ManyToManyField(OrderProductInfo)
    order_status = models.CharField(max_length=100, choices=orderstatus_choice)
    order_payment_type = models.CharField(max_length=100, choices=oderpayment_choice)
    order_payment_status = models.CharField(max_length=100, choices=orderpaymentstatus_choice)
    total_order_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    custom_payment_ref = models.OneToOneField(CustomePaymentMethod, models.SET_NULL, blank=True, null=True)
    courier_detail_ref = models.OneToOneField(CourierDetail, models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return str(self.id)


class CartProductInfo(models.Model):
    product = models.ForeignKey(Products, models.SET_NULL, blank=True, null=True)
    product_quantity = models.IntegerField()
    single_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_product_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.product_title


class Cart(models.Model):
    products_cart = models.ManyToManyField(CartProductInfo)
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)




