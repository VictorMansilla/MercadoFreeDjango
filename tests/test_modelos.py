import datetime
import pytest
from DjangoApp.models import Producto, Registro_Productos, Registro_Usuarios, Usuario
#from rest_framework.test import APIClient


@pytest.mark.django_db
def testModeloUsuario():
    usuario = Usuario(nombre_usuario = 'usuario1',
                      contrasegna_usuario = 'usuario1')
    
    assert usuario



@pytest.mark.django_db
def testModeloProducto():
    usuario = Usuario(nombre_usuario = 'usuario1',
                      contrasegna_usuario = 'usuario1')

    producto = Producto(producto_nombre = 'producto1',
                        producto_precio = 1,
                        producto_usuario = usuario)
    
    assert producto



@pytest.mark.django_db
def testModeloRegistroUsuario():
    registro = Registro_Usuarios(accion_nombre = 'agregar',
                                 accion_usuario_id = 1,
                                 accion_usuario_nombre = 'usuario1',
                                 accion_momento = datetime.datetime.utcnow())
    
    assert registro



@pytest.mark.django_db
def testModeloRegistroProducto():
    registro = Registro_Productos(accion_nombre = 'agregar',
                                 accion_usuario_id = 1,
                                 accion_usuario_nombre = 'usuario1',
                                 accion_producto_id = 1,
                                 accion_momento = datetime.datetime.utcnow())
    
    assert registro
