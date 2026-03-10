from django.contrib import admin
from .models import Task


class taskAdmin(admin.ModelAdmin):
    # Campo de solo lectura
    # Muestra la fecha de creacion de la tarea
    readonly_fields = ("created", ) 

# Register your models here.
admin.site.register(Task, taskAdmin)