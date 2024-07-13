from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.CharField(null=False, max_length=200)
    contrasegna_usuario = models.CharField(null=False, max_length=300)
    email_usuario = models.EmailField(max_length=30)
    telefono_usuario = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre_usuario

class Producto(models.Model):
    producto_nombre = models.CharField(null=False, max_length=100)
    producto_precio = models.IntegerField(null=False)
    producto_descripcion = models.CharField(max_length=700)
    producto_usuario = models.IntegerField(null=False)

    def __str__(self):
        return self.producto_nombre
