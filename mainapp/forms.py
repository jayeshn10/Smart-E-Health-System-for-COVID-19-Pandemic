from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.forms import TextInput, EmailInput, FileInput, PasswordInput, CharField, Textarea, Select, CheckboxInput, \
    HiddenInput, DateTimeInput

from mainapp.models import User, Blogs, Appointments, Orders, CustomePaymentMethod, Products, ProductImage


class CreateUserAdminForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    user_image = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control-file'}))
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['password', ]

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image


class ChangeUserAdminForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = '__all__'

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = ''
            return user_image


class EditUserDetailsForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'user_mobile', 'user_address', 'user_image']

        widgets = {

            "first_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "last_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email"
                }),
            "user_mobile": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "user_address": Textarea(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = ''
            return user_image


class UserChangePasswordCustom(SetPasswordForm):
    new_password1 = CharField(required=True, label='newpassword',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'The password can not be empty'})
    new_password2 = CharField(required=True, label='confirmpassword',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'The password can not be empty'})


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['blog_title', 'blog_slug', 'blog_desc', 'blog_publish', 'blog_img']

        widgets = {

            "blog_title": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "blog_slug": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "blog_desc": Textarea(
                attrs={
                    "class": "form-control"
                }),
            "blog_publish": CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }),

            "blog_img": FileInput(
                attrs={
                    "class": "form-control-file"
                }),

        }


class EditBlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['blog_title', 'blog_slug', 'blog_desc', 'blog_publish', 'blog_img']

        widgets = {

            "blog_title": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "blog_slug": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "blog_desc": Textarea(
                attrs={
                    "class": "form-control"
                }),
            "blog_publish": CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }),

        }

    def clean_blog_img(self):
        blog_img = self.cleaned_data['blog_img']
        if blog_img:
            return blog_img
        else:
            blog_img = 'emptyfile'
            return blog_img


class AddUserForm(UserCreationForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    user_image = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control-file'}))
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_mobile', 'user_address', 'user_image'
            , 'is_hospital_staff', 'is_patient', 'is_doctor', 'password1', 'password2']

        widgets = {

            "first_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "last_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "type": "email"
                }),
            "user_mobile": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "user_address": Textarea(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_user_image(self):
        user_image = self.cleaned_data['user_image']
        if user_image:
            return user_image
        else:
            user_image = 'profileimages/user.png'
            return user_image


class AddAppointment(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['patient', 'p_h_problem', 'doctor', ]

        widgets = {
            "p_h_problem": Textarea(
                attrs={
                    "class": "form-control",
                    "required": True,
                }),
            "doctor": Select(
                attrs={
                    "class": "form-control",
                    "required": True,
                }),

        }


class EditAppointment(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['p_h_problem', 'a_status', 'a_date_time', 'a_meeting_id', 'checkup_report',
                  'checkup_report_file', 'd_prescription']

        widgets = {
            "p_h_problem": Textarea(
                attrs={
                    "class": "form-control",
                }),
            "a_status": Select(
                attrs={
                    "class": "form-control",
                }),
            "a_date_time": TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                }),
            "a_meeting_id": TextInput(
                attrs={
                    "class": "form-control",
                }),
            "checkup_report": Textarea(
                attrs={
                    "class": "form-control",
                }),
            "d_prescription": Textarea(
                attrs={
                    "class": "form-control",
                }),

        }


class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ["customer_name", "customer_address", "customer_contry", "customer_state", "customer_city", "city_zip",
                  "customer_email", "customer_mobile_number"]

        widgets = {
            "customer_name": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "customer_address": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                }),
            "customer_contry": Select(
                attrs={
                    "class": "custom-select d-block"
                }),
            "customer_state": TextInput(
                attrs={
                    "class": "form-control d-block"
                }),
            "customer_city": TextInput(
                attrs={
                    "class": "form-control d-block"
                }),
            "city_zip": TextInput(
                attrs={
                    "class": "form-control d-block"
                }),
            "customer_email": EmailInput(
                attrs={
                    "class": "form-control",
                    'placeholder': 'you@example.com'
                }),
            "customer_mobile_number": TextInput(
                attrs={
                    "class": "form-control",
                    'type': 'number'
                }),
        }


class AddCustomePaymentMethodForm(forms.ModelForm):
    class Meta:
        model = CustomePaymentMethod
        fields = ["upi_transaction_id", "upi_id", "payment_proof"]

        widgets = {
            "upi_transaction_id": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "upi_id": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "payment_proof": FileInput(
                attrs={
                    "class": "file-field"
                }),

        }


class CartFrom(forms.Form):
    products_cart = forms.CharField(max_length=1000, widget=forms.HiddenInput())


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_title', 'product_desc', 'product_price', 'product_count', 'product_img']

        widgets = {
            "product_title": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "product_price": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "product_count": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "product_desc": Textarea(
                attrs={
                    "class": "form-control"
                }),

        }


class EditProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['product_title', 'product_desc', 'product_price', 'product_count', 'product_img']

        widgets = {
            "product_title": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "product_price": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "product_count": TextInput(
                attrs={
                    "class": "form-control"
                }),
            "product_desc": Textarea(
                attrs={
                    "class": "form-control"
                }),

        }

    def clean_product_img(self):
        product_img = self.cleaned_data['product_img']
        if product_img:
            return product_img
        else:
            product_img = 'emptyfile'
            return product_img


class AddProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_images', ]
