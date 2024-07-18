from django.contrib import admin
from .models import Producto, Usuario

# Register your models here.
class Datos_Usuario(admin.ModelAdmin):
    # ...
    list_display = ["nombre_usuario", "contrasegna_usuario", "email_usuario", "telefono_usuario"]

class Datos_Producto(admin.ModelAdmin):
    # ...
    list_display = ["producto_nombre", "producto_precio", "producto_descripcion", "producto_usuario"]

admin.site.register(Usuario, Datos_Usuario)
admin.site.register(Producto, Datos_Producto)
