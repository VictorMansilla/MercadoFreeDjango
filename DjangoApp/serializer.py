from rest_framework import serializers

from .models import Usuario, Producto

class UsuariooSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre_usuario', 'contraseña_usuario', 'email_usuario', 'telefono']
        read_only_fields = ['id']


class ProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'producto_nombre', 'producto_precio', 'producto_descripcion', 'producto_usuario']
        read_only_fields = ['id', 'producto_usuario']
