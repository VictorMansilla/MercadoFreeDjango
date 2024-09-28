from django.db import models



class Usuario(models.Model):
    nombre_usuario = models.CharField(null=False, max_length=200, unique=True)
    contrasegna_usuario = models.CharField(null=False, max_length=300)
    email_usuario = models.EmailField(null=True, max_length=30)
    telefono_usuario = models.CharField(null=True, max_length=15)

    def __str__(self):
        return self.nombre_usuario



class Producto(models.Model):
    producto_nombre = models.CharField(null=False, max_length=100)
    producto_precio = models.IntegerField(null=False)
    producto_descripcion = models.CharField(null=True, max_length=700)
    producto_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.producto_nombre



class Registro_Usuarios(models.Model):
    accion_opciones = [
        ('agregar', 'Agregar'),
        ('borrar', 'Borrar'),
        ('editar', 'Editar'),
        ('ingresar', 'Ingresar'),]
    accion_nombre = models.CharField(null=True, max_length=10, choices=accion_opciones, default=None)
    accion_usuario_id = models.IntegerField(null=False)
    accion_usuario_nombre = models.CharField(null=False, max_length=200)
    accion_momento = models.TimeField(null=False)

    def __str__(self):
        return self.accion_nombre



class Registro_Productos(models.Model):
    accion_opciones = [
        ('agregar', 'Agregar'),
        ('borrar', 'Borrar'),
        ('editar', 'Editar'),]
    accion_nombre = models.CharField(null=True, max_length=10, choices=accion_opciones, default=None)
    accion_usuario_id = models.IntegerField(null=False)
    accion_usuario_nombre = models.CharField(null=False, max_length=200)
    accion_producto_id = models.IntegerField(null=False)
    accion_momento = models.TimeField(null=False)

    def __str__(self):
        return self.accion_nombre