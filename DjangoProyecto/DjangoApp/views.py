from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Usuario, Producto
from .serializer import ProductoSerializers

import bcrypt
import jwt
import secrets
import datetime

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt

@api_view(['POST'])
def Crear_Usuario(request):
    datos = request.data
    if datos:
        nombre_usuario = datos['nombre_usuario']

        if Usuario.objects.filter(nombre_usuario = nombre_usuario).exists() is False:
            contrasegna_usuario = datos['contrasegna_usuario']
            email_usuario = datos['email_usuario']
            telefono_usuario = datos['telefono_usuario']

            Contrasegna_en_bytes =  contrasegna_usuario.encode('utf-8')   #Encoding de la contraseña en formato bytes
            Contrasegna_Hasheada = bcrypt.hashpw(Contrasegna_en_bytes, bcrypt.gensalt())   #Hashear la contraseña en formato bytes, en el ingreso a la base de datos de decodea la contraseña para almacenarla en la base de datos

            ingreso_usuario_database = Usuario(nombre_usuario = nombre_usuario, contrasegna_usuario = Contrasegna_Hasheada.decode('utf-8'), email_usuario = email_usuario, telefono_usuario = telefono_usuario)
            ingreso_usuario_database.save()
            return Response({'Completado':'El usuario fue ingresado'}, status=status.HTTP_201_CREATED)

        else:return Response({'Inválido':'El usuario ya existe'}, status=status.HTTP_302_FOUND)

    else:return Response({'Error':'Surgió algún error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)



segundos_exp = 2000
clave_secreta = secrets.token_hex(62)
algoritmo = ['HS256']

def Generar_Token(nombre_usuario_token, id_usuario_token):
    payload = {
        'Id_usuario' : id_usuario_token,
        'nombre_usuario' : nombre_usuario_token,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=segundos_exp)}
    token = jwt.encode(payload, clave_secreta, algorithm='HS256')
    print(token)
    return token



@api_view(['GET'])
def Validar_Usuario(request):
    datos = request.data
    nombre_usuario = datos['nombre_usuario']

    if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
        contrasegna_usuario = datos['contrasegna_usuario']
        datos_usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)

        if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
            token = Generar_Token(datos_usuario.nombre_usuario, datos_usuario.id)
            return Response({'Si se puede':'Contraseña válida', 'token' : f'{token}'}, status=status.HTTP_200_OK)

        else:return Response({'Si se puede':'Contraseña inválida'}, status=status.HTTP_201_CREATED)
    
    else:return Response({'No se puede':'Usuario inálido'}, status=status.HTTP_302_FOUND)
    


@api_view(['POST'])
def Actualizar_Usuario(request):
    datos = request.data
    token = datos['token']

    try:
        token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)
        nuevo_nombre_usuario = datos['nuevo_nombre_usuario']

        if Usuario.objects.filter(nombre_usuario = nuevo_nombre_usuario).exists() is False:
            contrasegna_usuario = datos['contrasegna_usuario']

            datos_usuario = Usuario.objects.get(nombre_usuario = token_deployado['nombre_usuario'])

            if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
                nueva_contrasegna_usuario = datos['nueva_contrasegna_usuario']
                nuevo_email_usuario = datos['nuevo_email_usuario']
                nuevo_telefono_usuario = datos['nuevo_telefono_usuario']

                contrasegna_en_bytes =  nueva_contrasegna_usuario.encode('utf-8')
                contrasegna_Hasheada = bcrypt.hashpw(contrasegna_en_bytes, bcrypt.gensalt())

                datos_usuario.nombre_usuario = nuevo_nombre_usuario
                datos_usuario.contrasegna_usuario = contrasegna_Hasheada
                datos_usuario.email_usuario = nuevo_email_usuario
                datos_usuario.telefono_usuario = nuevo_telefono_usuario
                datos_usuario.save()
                return Response({'Completado':'Datos del usuario actualizados'}, status=status.HTTP_200_OK)
                
            else:return Response({'Si se puede':'Contraseña inválida'}, status=status.HTTP_201_CREATED)

        else:return Response({'Inválido':'El usuario ya existe'}, status=status.HTTP_302_FOUND)
    
    except jwt.ExpiredSignatureError:
        return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
    except jwt.InvalidTokenError:
        return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)



@api_view(['POST'])
def Eliminar_Usuario(request):
    datos = request.data
    token = datos['token']

    try:
        token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)

        if Usuario.objects.filter(nombre_usuario = token_deployado['nombre_usuario']).exists():
            datos_usuario = Usuario.objects.get(nombre_usuario=token_deployado['nombre_usuario'])
            contrasegna_usuario = datos['contrasegna_usuario']

            if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
                usuario_a_eliminar = Usuario.objects.filter(id = token_deployado['Id_usuario'])
                usuario_a_eliminar.delete()
                return Response({'Completado':'Usuario eliminado'}, status=status.HTTP_200_OK)

            else:return Response({'Si se puede':'Contraseña inválida'}, status=status.HTTP_201_CREATED)
        
        else:return Response({'Inválido':'El usuario no existe'}, status=status.HTTP_302_FOUND)

    except jwt.ExpiredSignatureError:
        return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
    except jwt.InvalidTokenError:
        return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)



@api_view(['POST'])
def Crear_Producto(request):
    datos = request.data
    producto_nombre = datos['producto_nombre']
    producto_precio = datos['producto_precio']
    producto_descripcion = datos['producto_descripcion']
    token = datos['token']

    try:
        token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)

        ingresar_producto_database = Producto(producto_nombre = producto_nombre, producto_precio = producto_precio, producto_descripcion = producto_descripcion, producto_usuario = token_deployado['Id_usuario'])
        ingresar_producto_database.save()
        
        return Response({'Completado':'El producto fue ingresado'}, status=status.HTTP_201_CREATED)
    
    except jwt.ExpiredSignatureError:
        return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    except jwt.InvalidTokenError:
        return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)



@api_view(['POST'])
def Editar_Producto(request):
    datos = request.data
    token = datos['token']

    try:
        token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)
        id_producto = datos['id_producto']
        nuevo_producto_nombre = datos['nuevo_producto_nombre']
        nuevo_producto_precio = datos['nuevo_producto_precio']
        nueva_producto_descripcion = datos['nueva_producto_descripcion']

        datos_producto = Producto.objects.get(id = id_producto)
        datos_producto.producto_nombre = nuevo_producto_nombre
        datos_producto.producto_precio = nuevo_producto_precio
        datos_producto.producto_descripcion = nueva_producto_descripcion
        datos_producto.save()

        return Response({'Hecho' : "Producto actualizado"}, status=status.HTTP_205_RESET_CONTENT)

    except jwt.ExpiredSignatureError:
        return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    except jwt.InvalidTokenError:
        return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)
    


@api_view(['POST'])
def Eliminar_Producto(request):
    datos = request.data
    token = datos['token']

    try:
        token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)
        id_producto = datos['id_producto']
        producto_a_eliminar = Producto.objects.filter(id = id_producto)
        producto_a_eliminar.delete()
        return Response({'Hecho' : "El producto fue eliminado"}, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    except jwt.InvalidTokenError:
        return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)



@api_view(['GET'])
def Obtener_Productos(request):
    datos = Producto.objects.all()
    productos = ProductoSerializers(datos, many=True)
    return Response(productos.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def Obtener_un_Producto(request, ID_Producto):
    datos = Producto.objects.filter(id=ID_Producto)
    productos = ProductoSerializers(datos, many=True)
    return Response(productos.data, status=status.HTTP_200_OK)



#    data = [{"id": item.id, "name": item.name, "description": item.description} for item in items]

