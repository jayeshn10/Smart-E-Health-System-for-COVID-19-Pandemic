from django.contrib import admin

# Register your models here.
from mainapp.forms import ChangeUserAdminForm, CreateUserAdminForm
from mainapp.models import User, Blogs, Appointments, PtoSNotification, StoPNotification, StoDNotification, \
    DtoPNotification, ProductImage, Products, OrderProductInfo, CustomePaymentMethod, Orders, CartProductInfo, Cart, \
    CourierDetail


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form = ChangeUserAdminForm
    add_form = CreateUserAdminForm

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(UserAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Blogs)
admin.site.register(Appointments)
admin.site.register(PtoSNotification)
admin.site.register(StoPNotification)
admin.site.register(StoDNotification)
admin.site.register(DtoPNotification)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):


    inlines = [ProductImageAdmin]
    list_per_page = 10
    ordering = ['id']

    list_display = ('product_title',)

    class Meta:
        model = Products



admin.site.register(OrderProductInfo)
admin.site.register(CustomePaymentMethod)
admin.site.register(Orders)
admin.site.register(CartProductInfo)
admin.site.register(Cart)
admin.site.register(CourierDetail)