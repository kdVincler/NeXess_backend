from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Door, Permission, Log

# Register your models here.

# Reworked according to https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#modeladmin-objects 

@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    """Class representation of the Door model in the admin interface"""
    search_fields = ('descriptor',)
    list_display = ('id', 'descriptor', 'perm_level')
    list_filter = ('perm_level',)
    list_per_page = 25
    ordering= ('perm_level',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Class representation of the Permission model in the admin interface"""
    search_fields = ('user__username', 'user__first_name', 'user__last_name',)
    list_display = ('full_name', 'user', 'perm_level',)
    list_filter = ('perm_level',)
    list_per_page = 25
    ordering= ('perm_level', 'user__last_name', 'user__first_name',)

    @admin.display(description="Name",)
    def full_name(self, obj):
        """Property to display the full name of the user on the admin site"""
        return obj.user.first_name + " " + obj.user.last_name


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """Class representation of the Log model in the admin interface"""
    search_fields = ('user__username', 'door__descriptor', 'user__first_name', 'user__last_name',)
    list_display = ('full_name', 'user', 'door', 'date_time', 'perm_granted',)
    list_filter = ('user', 'door__id', 'date_time', 'perm_granted',)
    list_per_page = 25
    ordering= ('-date_time',)
    date_hierarchy = 'date_time'

    @admin.display(description="Name",)
    def full_name(self, obj):
        """Property to display the full name of the user on the admin site"""
        return obj.user.first_name + " " + obj.user.last_name


class CustomUserAdmin(UserAdmin):
    """Custom user admin to edit what fields show up on account creation and to edit what and how is displayed"""
    list_display = ('username', 'last_name', 'first_name', 'is_staff',)
    ordering= ('last_name', 'first_name', 'username',)
    # https://stackoverflow.com/questions/50436596/what-is-add-fieldsets-for-in-useradmin-in-django
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name',  'is_staff', 'is_superuser')}
        ),
    )
    # https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#modeladmin-methods
    def save_model(self, request, obj, form, change):
        """Function to automatically create a Permission instance linked to the created user"""
        super().save_model(request, obj, form, change)
        new_user = User.objects.get(id=obj.id)
        Permission.objects.create(user=new_user, perm_level=0)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.unregister(Group)