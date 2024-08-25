from django.contrib import admin
from .models import Producto, Usuario, Registro_Usuarios, Registro_Productos

# Register your models here.
class Datos_Usuario(admin.ModelAdmin):
    # ...
    list_display = ["id", "nombre_usuario", "contrasegna_usuario", "email_usuario", "telefono_usuario"]

class Datos_Producto(admin.ModelAdmin):
    # ...
    list_display = ["id", "producto_nombre", "producto_precio", "producto_descripcion", "producto_usuario"]

class Registro_del_Usuario(admin.ModelAdmin):
    # ...
    list_display = ["id", "accion_nombre", "accion_usuario_id", "accion_usuario_nombre", "accion_momento"]

class Registro_de_Producto(admin.ModelAdmin):
    # ...
    list_display = ["id", "accion_nombre", "accion_usuario_id", "accion_usuario_nombre", "accion_producto_id", "accion_momento"]

admin.site.register(Usuario, Datos_Usuario)
admin.site.register(Producto, Datos_Producto)
admin.site.register(Registro_Usuarios, Registro_del_Usuario)
admin.site.register(Registro_Productos, Registro_de_Producto)