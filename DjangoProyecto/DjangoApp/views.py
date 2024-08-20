from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
#from typing import List, Dict

from .models import Usuario, Producto, Registro_Usuarios
from .serializer import ProductoSerializers
from .token import Generar_Token, clave_secreta, algoritmo

import bcrypt
import jwt
import datetime
import redis
import os

redis_instance = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

@api_view(['POST'])
def Crear_Usuario(request):
    try:
        datos = request.data
        if datos:
            nombre_usuario:str = datos['nombre_usuario']

            if Usuario.objects.filter(nombre_usuario = nombre_usuario).exists() is False:
                contrasegna_usuario:str = datos['contrasegna_usuario']
                email_usuario:str = datos.get('email_usuario', None)
                telefono_usuario:int = datos.get('telefono_usuario', None)

                Contrasegna_en_bytes:str =  contrasegna_usuario.encode('utf-8')   #Encoding de la contraseña en formato bytes
                Contrasegna_Hasheada:str = bcrypt.hashpw(Contrasegna_en_bytes, bcrypt.gensalt())   #Hashear la contraseña en formato bytes, en el ingreso a la base de datos de decodea la contraseña para almacenarla en la base de datos

                ingreso_usuario_database = Usuario(nombre_usuario = nombre_usuario, contrasegna_usuario = Contrasegna_Hasheada.decode('utf-8'), email_usuario = email_usuario, telefono_usuario = telefono_usuario)
                ingreso_usuario_database.save()

                usuario = Usuario.objects.get(nombre_usuario = nombre_usuario)

                crear_registro = Registro_Usuarios(accion_nombre = 'agregar', accion_usuario_id = usuario.id, accion_usuario_nombre = nombre_usuario, accion_momento = datetime.datetime.utcnow())
                crear_registro.save()
                return Response({'Completado':'El usuario fue ingresado'}, status=status.HTTP_201_CREATED)

            else:return Response({'Inválido':'El usuario ya existe'}, status=status.HTTP_302_FOUND)

        else:return Response({'Error':'Surgió algún error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def Validar_Usuario(request):
    try:
        datos = request.data
        nombre_usuario:str = datos['nombre_usuario']

        if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
            contrasegna_usuario:str = datos['contrasegna_usuario']
            datos_usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)

            if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
                token:str = Generar_Token(datos_usuario.nombre_usuario, datos_usuario.id)
                crear_registro = Registro_Usuarios(accion_nombre = 'ingresar', accion_usuario_id = datos_usuario.id, accion_usuario_nombre = datos_usuario.nombre_usuario, accion_momento = datetime.datetime.utcnow())
                crear_registro.save()
                return Response({'Si se puede':'Contraseña válida', 'token' : f'{token}'}, status=status.HTTP_200_OK)

            else:return Response({'Si se puede':'Contraseña inválida'}, status=status.HTTP_201_CREATED)
        
        else:return Response({'No se puede':'Usuario inálido'}, status=status.HTTP_302_FOUND)

    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Desvalidar_Usuario(request):
    datos = request.data
    token:str = datos.get('token')
    expiration_time = os.environ.get('segundos_exp')
    redis_instance.setex(token, expiration_time, "revoked")
    return Response({'Completado':'Usuario deslogueado'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def Actualizar_Usuario(request):
    try:
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
                    nuevo_email_usuario = datos.get('nuevo_email_usuario', None)
                    nuevo_telefono_usuario = datos.get('nuevo_telefono_usuario', None)

                    contrasegna_en_bytes =  nueva_contrasegna_usuario.encode('utf-8')
                    contrasegna_Hasheada = bcrypt.hashpw(contrasegna_en_bytes, bcrypt.gensalt())

                    datos_usuario.nombre_usuario = nuevo_nombre_usuario
                    datos_usuario.contrasegna_usuario = contrasegna_Hasheada.decode('utf-8')
                    datos_usuario.email_usuario = nuevo_email_usuario
                    datos_usuario.telefono_usuario = nuevo_telefono_usuario
                    datos_usuario.save()
                    crear_registro = Registro_Usuarios(accion_nombre = 'editar', accion_usuario_id = datos_usuario.id, accion_usuario_nombre = datos_usuario.nombre_usuario, accion_momento = datetime.datetime.utcnow())
                    crear_registro.save()
                    return Response({'Completado':'Datos del usuario actualizados'}, status=status.HTTP_200_OK)
                    
                else:return Response({'Si se puede':'Contraseña inválida'}, status=status.HTTP_201_CREATED)

            else:return Response({'Inválido':'El usuario ya existe'}, status=status.HTTP_302_FOUND)
        
        except jwt.ExpiredSignatureError:
            return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
        except jwt.InvalidTokenError:
            return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)
        
    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Eliminar_Usuario(request):
    try:
        datos = request.data
        token = datos['token']

        try:
            token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)

            if redis_instance.get(token) != b"revoked":

                if Usuario.objects.filter(nombre_usuario = token_deployado['nombre_usuario']).exists():
                    datos_usuario = Usuario.objects.get(nombre_usuario=token_deployado['nombre_usuario'])
                    contrasegna_usuario = datos['contrasegna_usuario']

                    if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
                        usuario_a_eliminar = Usuario.objects.get(id = token_deployado['Id_usuario'])
                        usuario_a_eliminar.delete()
                        eliminar_productos_usuario = Producto.objects.get(producto_usuario = token_deployado['Id_usuario'])
                        eliminar_productos_usuario.delete()
                        crear_registro = Registro_Usuarios(accion_nombre = 'borrar', accion_usuario_id = datos_usuario.id, accion_usuario_nombre = datos_usuario.nombre_usuario, accion_momento = datetime.datetime.utcnow())
                        crear_registro.save()
                        return Response({'Completado':'Usuario eliminado'}, status=status.HTTP_200_OK)

                    else:return Response({'Si se puede':'Contraseña inválida'}, status=status.HTTP_201_CREATED)
                
                else:return Response({'Inválido':'El usuario no existe'}, status=status.HTTP_302_FOUND)

            else:return Response({'Completado':'Usuario deslogueado'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
        except jwt.InvalidTokenError:
            return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)
        
    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Crear_Producto(request):
    try:
        datos = request.data
        token = datos['token']
        producto_nombre = datos['producto_nombre']
        producto_precio = datos['producto_precio']
        producto_descripcion = datos.get('producto_descripcion', None)

        try:
            print(token)
            print(clave_secreta)
            print(algoritmo)
            token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)

            ingresar_producto_database = Producto(producto_nombre = producto_nombre, producto_precio = producto_precio, producto_descripcion = producto_descripcion, producto_usuario = token_deployado['Id_usuario'])
            ingresar_producto_database.save()
            crear_registro = Registro_Usuarios(accion_nombre = 'agregar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_momento = datetime.datetime.utcnow())
            crear_registro.save()
            return Response({'Completado':'El producto fue ingresado'}, status=status.HTTP_201_CREATED)
        
        except jwt.ExpiredSignatureError:
            return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        except jwt.InvalidTokenError:
            return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)
        
    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Editar_Producto(request):
    try:
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
            crear_registro = Registro_Usuarios(accion_nombre = 'editar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_momento = datetime.datetime.utcnow())
            crear_registro.save()
            return Response({'Hecho' : "Producto actualizado"}, status=status.HTTP_205_RESET_CONTENT)

        except jwt.ExpiredSignatureError:
            return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        except jwt.InvalidTokenError:
            return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)
        
    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)    



@api_view(['POST'])
def Eliminar_Producto(request):
    try:
        datos = request.data
        token = datos['token']

        try:
            token_deployado = jwt.decode(token, clave_secreta, algorithms=algoritmo)
            id_producto = datos['id_producto']
            producto_a_eliminar = Producto.objects.filter(id = id_producto)
            producto_a_eliminar.delete()
            crear_registro = Registro_Usuarios(accion_nombre = 'borrar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_momento = datetime.datetime.utcnow())
            crear_registro.save()
            return Response({'Hecho' : "El producto fue eliminado"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'Error' : "El token a expirado"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        except jwt.InvalidTokenError:
            return Response({'Error' : "Error en la validación del token"}, status=status.HTTP_409_CONFLICT)
        
    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def Obtener_Productos(request):
    datos = Producto.objects.all()
    productos = ProductoSerializers(datos, many=True)
    return Response(productos.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def Obtener_un_Producto(request, ID_Producto):
    try:
        datos = Producto.objects.filter(id=ID_Producto)
        productos = ProductoSerializers(datos, many=True)
        return Response(productos.data, status=status.HTTP_200_OK)
    
    except ValueError:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)



from django.db.models import Q

@api_view(['GET'])
def Buscar_producto(request):
    try:
        datos = request.data
        print(datos)

        if datos:
            query = datos['query']
            print(query)
            productos = Producto.objects.filter(Q(producto_nombre__icontains=query))
            print(productos)
            pro = ProductoSerializers(productos, many=True)
            print(pro.data)
            return Response(pro.data, status=status.HTTP_200_OK)
            
        else:return Response({'Error':'1'}, status=status.HTTP_400_BAD_REQUEST)
        
    except:
        return Response({'Error':'No hay valores requeridos'}, status=status.HTTP_400_BAD_REQUEST)

