from django.contrib import admin

# Register your models here.
from mainapp.forms import ChangeUserAdminForm, CreateUserAdminForm
from mainapp.models import User, Blogs, Appointments, PtoSNotification, StoPNotification, StoDNotification, \
    DtoPNotification


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

