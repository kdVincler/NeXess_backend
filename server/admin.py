from django.contrib import admin
from .models import Door, Permission, Log

# Register your models here.
admin.site.register(Door)
admin.site.register(Permission)
admin.site.register(Log)