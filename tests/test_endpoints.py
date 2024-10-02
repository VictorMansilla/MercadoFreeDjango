import pytest

from rest_framework.test import APIClient

@pytest.mark.django_db
def testCrearUsuario():
    cliente = APIClient()
    request = {
        "nombre_usuario" : "usuario1",
        "contrasegna_usuario" : "usuario1"
    }
    respuesta = cliente.post("/DjangoApp/Crear_Usuario/", request, format="json")

    assert respuesta.status_code == 201



@pytest.mark.django_db
def testValidarUsuario():
    testCrearUsuario()
    cliente = APIClient()
    request = {
        "nombre_usuario" : "usuario1",
        "contrasegna_usuario" : "usuario1"
    }
    respuesta = cliente.post("/DjangoApp/Validar_Usuario/", request, format="json")

    assert respuesta.status_code == 200
