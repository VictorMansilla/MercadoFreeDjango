from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from typing import List, Dict

from .models import Usuario, Producto, Registro_Usuarios, Registro_Productos
from .serializer import ProductoSerializers
from .token import Deployar_Token, Generar_Token

import bcrypt
import datetime
import redis
import os

redis_instance = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

lista_carrito:list = []

@api_view(['POST'])
def Crear_Usuario(request):
    try:
        datos:Dict = request.data
        nombre_usuario:str = datos['nombre_usuario']
        
        if Usuario.objects.filter(nombre_usuario = nombre_usuario).exists() is False:
            contrasegna_usuario:str = datos['contrasegna_usuario']
            email_usuario:str = datos.get('email_usuario', None)
            telefono_usuario:int = datos.get('telefono_usuario', None)

            Contrasegna_en_bytes:bytes =  contrasegna_usuario.encode('utf-8')   #Encoding de la contraseña en formato bytes
            Contrasegna_Hasheada:str = bcrypt.hashpw(Contrasegna_en_bytes, bcrypt.gensalt())   #Hashear la contraseña en formato bytes, en el ingreso a la base de datos de decodea la contraseña para almacenarla en la base de datos
            ingreso_usuario_database = Usuario(nombre_usuario = nombre_usuario, contrasegna_usuario = Contrasegna_Hasheada.decode('utf-8'), email_usuario = email_usuario, telefono_usuario = telefono_usuario)
            
            ingreso_usuario_database.save()
            usuario = Usuario.objects.get(nombre_usuario = nombre_usuario)
            crear_registro = Registro_Usuarios(accion_nombre = 'agregar', accion_usuario_id = usuario.id, accion_usuario_nombre = nombre_usuario, accion_momento = datetime.datetime.utcnow())
            crear_registro.save()
            return Response({'Completado':'El usuario fue ingresado'}, status=status.HTTP_201_CREATED)
        
        else:return Response({'Inválido':'El usuario ya existe'}, status=status.HTTP_302_FOUND)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Validar_Usuario(request):
    try:
        datos:Dict = request.data
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
        
        else:return Response({'Error':'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Desvalidar_Usuario(request):
    try:
        auth_headre = request.headers.get('Authorization')

        if auth_headre is None or not auth_headre.startswith('Bearer '):
            return Response({'Error': 'Token no provisto en el header'}, status=status.HTTP_400_BAD_REQUEST)
        token:str = auth_headre.split(' ')[1]

        if redis_instance.get(token) != b'revoked':
            token_payload = Deployar_Token(token)
            expiration_time = os.environ.get('segundos_exp')
            redis_instance.setex(token, expiration_time, "revoked")
            return Response({'Completado':'Usuario deslogueado'}, status=status.HTTP_200_OK)
        
        else:return Response({'Error':'Usuario no logueado'}, status=status.HTTP_423_LOCKED)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:return Response({'Error': f'Ocurrió un error en el servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
def Actualizar_Usuario(request):
    try:
        datos:Dict = request.data
        auth_headre = request.headers.get('Authorization')

        if auth_headre is None or not auth_headre.startswith('Bearer '):
            return Response({'Error': 'Token no provisto en el header'}, status=status.HTTP_400_BAD_REQUEST)
        token:str = auth_headre.split(' ')[1]

        if redis_instance.get(token) != b'revoked':
            token_deployado = Deployar_Token(token)

            if Usuario.objects.filter(nombre_usuario = token_deployado['nombre_usuario']).exists():
                contrasegna_usuario = datos['contrasegna_usuario']
                datos_usuario = Usuario.objects.get(nombre_usuario = token_deployado['nombre_usuario'])


                if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
                    nueva_contrasegna_usuario:str = datos['nueva_contrasegna_usuario']
                    
                    if nueva_contrasegna_usuario != None:
                        contrasegna_en_bytes:bytes =  nueva_contrasegna_usuario.encode('utf-8')
                        contrasegna_Hasheada:str = bcrypt.hashpw(contrasegna_en_bytes, bcrypt.gensalt())
                        datos_usuario.contrasegna_usuario = contrasegna_Hasheada.decode('utf-8')


                    nuevo_email_usuario:str = datos.get('nuevo_email_usuario', datos_usuario.email_usuario)
                    nuevo_telefono_usuario:str = datos.get('nuevo_telefono_usuario', datos_usuario.telefono_usuario)


                    datos_usuario.email_usuario = nuevo_email_usuario
                    datos_usuario.telefono_usuario = nuevo_telefono_usuario
                    nuevo_nombre_usuario:str = datos.get('nuevo_nombre_usuario', datos_usuario.nombre_usuario)

                    if nuevo_nombre_usuario != datos_usuario.nombre_usuario:

                        if Usuario.objects.filter(nombre_usuario = nuevo_nombre_usuario).exists() is False:
                            datos_usuario.nombre_usuario = nuevo_nombre_usuario

                        else:return Response({'Error':'Ese nombre de usuario ya se encuentra ocupado'}, status=status.HTTP_306_RESERVED)

                    datos_usuario.save()
                    crear_registro = Registro_Usuarios(accion_nombre = 'editar', accion_usuario_id = datos_usuario.id, accion_usuario_nombre = datos_usuario.nombre_usuario, accion_momento = datetime.datetime.utcnow())
                    crear_registro.save()
                    return Response({'Completado':'Datos del usuario actualizados'}, status=status.HTTP_200_OK)
                    
                else:return Response({'Error':'Contraseña inválida'}, status=status.HTTP_401_UNAUTHORIZED)

            else:return Response({'Error':'El usuario no existe'}, status=status.HTTP_306_RESERVED)

        else:return Response({'Error':'Usuario no logueado'}, status=status.HTTP_423_LOCKED)
        
    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:return Response({'Error': f'Ocurrió un error en el servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def Eliminar_Usuario(request):
    try:
        datos:Dict = request.data
        auth_headre = request.headers.get('Authorization')

        if auth_headre is None or not auth_headre.startswith('Bearer '):
            return Response({'Error': 'Token no provisto en el header'}, status=status.HTTP_400_BAD_REQUEST)
        token:str = auth_headre.split(' ')[1]
        
        if redis_instance.get(token) != b"revoked":
            token_deployado = Deployar_Token(token)

            if Usuario.objects.filter(nombre_usuario = token_deployado['nombre_usuario']).exists():
                datos_usuario = Usuario.objects.get(nombre_usuario=token_deployado['nombre_usuario'])
                contrasegna_usuario:str = datos['contrasegna_usuario']

                if bcrypt.checkpw(contrasegna_usuario.encode('utf-8') , datos_usuario.contrasegna_usuario.encode('utf-8')):
                    usuario_a_eliminar = Usuario.objects.get(id = token_deployado['Id_usuario'])

                    if Producto.objects.filter(producto_usuario = token_deployado['Id_usuario']).exists():
                        eliminar_productos_usuario = Producto.objects.filter(producto_usuario = token_deployado['Id_usuario'])
                        for producto in eliminar_productos_usuario:
                            crear_registro_productos = Registro_Productos(accion_nombre = 'borrar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_producto_id = producto.id, accion_momento = datetime.datetime.utcnow())
                            crear_registro_productos.save()
                    crear_registro = Registro_Usuarios(accion_nombre = 'borrar', accion_usuario_id = datos_usuario.id, accion_usuario_nombre = datos_usuario.nombre_usuario, accion_momento = datetime.datetime.utcnow())
                    crear_registro.save()
                    usuario_a_eliminar.delete()
                    return Response({'Hecho':'El usuario fue eliminado'}, status=status.HTTP_200_OK)

                else:return Response({'Error':'Contraseña inválida'}, status=status.HTTP_401_UNAUTHORIZED)
            
            else:return Response({'Error':'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
            
        else:return Response({'Error':'Usuario no logueado'}, status=status.HTTP_423_LOCKED)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:return Response({'Error': f'Ocurrió un error en el servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def Crear_Producto(request):
    try:
        datos:Dict = request.data
        auth_headre = request.headers.get('Authorization')

        if auth_headre is None or not auth_headre.startswith('Bearer '):
            return Response({'Error': 'Token no provisto en el header'}, status=status.HTTP_400_BAD_REQUEST)
        token:str = auth_headre.split(' ')[1]

        if redis_instance.get(token) != b"revoked":
            token_deployado = Deployar_Token(token)
            producto_nombre:str = datos['producto_nombre']
            producto_precio:int = datos['producto_precio']
            producto_descripcion:str = datos.get('producto_descripcion', None)
            usuario = Usuario.objects.get(id = token_deployado['Id_usuario'])
            ingresar_producto_database = Producto(producto_nombre = producto_nombre, producto_precio = producto_precio, producto_descripcion = producto_descripcion, producto_usuario = usuario)
            ingresar_producto_database.save()
            crear_registro_productos = Registro_Productos(accion_nombre = 'agregar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_producto_id = ingresar_producto_database.id, accion_momento = datetime.datetime.utcnow())
            crear_registro_productos.save()
            return Response({'Completado':'El producto fue ingresado'}, status=status.HTTP_201_CREATED)
        
        else:return Response({'Error':'Usuario no logueado'}, status=status.HTTP_423_LOCKED)
        
    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:return Response({'Error': f'Ocurrió un error en el servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
def Editar_Producto(request):
    try:
        datos:Dict = request.data
        auth_headre = request.headers.get('Authorization')

        if auth_headre is None or not auth_headre.startswith('Bearer '):
            return Response({'Error': 'Token no provisto en el header'}, status=status.HTTP_400_BAD_REQUEST)
        token:str = auth_headre.split(' ')[1]

        if redis_instance.get(token) != b"revoked":
            token_deployado = Deployar_Token(token)
            id_producto:int = datos['id_producto']
            nuevo_producto_nombre:str = datos['nuevo_producto_nombre']
            nuevo_producto_precio:int = datos['nuevo_producto_precio']
            nueva_producto_descripcion:str = datos.get('nueva_producto_descripcion', None)

            if Producto.objects.filter(id = id_producto).exists():
                datos_producto = Producto.objects.get(id = id_producto)
                datos_producto.producto_nombre = nuevo_producto_nombre
                datos_producto.producto_precio = nuevo_producto_precio
                datos_producto.producto_descripcion = nueva_producto_descripcion
                datos_producto.save()
                crear_registro_productos = Registro_Productos(accion_nombre = 'editar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_producto_id = id_producto, accion_momento = datetime.datetime.utcnow())
                crear_registro_productos.save()
                return Response({'Hecho' : "Producto actualizado"}, status=status.HTTP_205_RESET_CONTENT)

            else:return Response({'Error':'No existe ese producto'}, status=status.HTTP_404_NOT_FOUND)

        else:return Response({'Error':'Usuario no logueado'}, status=status.HTTP_423_LOCKED)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:return Response({'Error': f'Ocurrió un error en el servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def Eliminar_Producto(request):
    try:
        datos:Dict = request.data
        auth_headre = request.headers.get('Authorization')

        if auth_headre is None or not auth_headre.startswith('Bearer '):
            return Response({'Error': 'Token no provisto en el header'}, status=status.HTTP_400_BAD_REQUEST)
        token:str = auth_headre.split(' ')[1]

        if redis_instance.get(token) != b"revoked":
            token_deployado = Deployar_Token(token)
            id_producto = datos['id_producto']

            if Producto.objects.filter(id = id_producto).exists():
                producto_a_eliminar = Producto.objects.filter(id = id_producto)
                producto_a_eliminar.delete()
                crear_registro_productos = Registro_Productos(accion_nombre = 'borrar', accion_usuario_id = token_deployado['Id_usuario'], accion_usuario_nombre = token_deployado['nombre_usuario'], accion_producto_id = id_producto, accion_momento = datetime.datetime.utcnow())
                crear_registro_productos.save()
                return Response({'Hecho' : "El producto fue eliminado"}, status=status.HTTP_200_OK)

            else:return Response({'Error':'No existe ese producto'}, status=status.HTTP_404_NOT_FOUND)

        else:return Response({'Error':'Usuario no logueado'}, status=status.HTTP_423_LOCKED)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:return Response({'Error': f'Ocurrió un error en el servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def Obtener_Productos(request):
    try:
        datos = Producto.objects.all()
        productos = ProductoSerializers(datos, many=True)
        return Response(productos.data, status=status.HTTP_200_OK)

    except ValueError:return Response({'Error':'No se pudo obtener los productos'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def Obtener_un_Producto(request, ID_Producto):
    try:
        ID_Producto = int(ID_Producto)
        datos = Producto.objects.filter(id=ID_Producto)
        
        if datos.exists():
            productos = ProductoSerializers(datos, many=True)
            return Response(productos.data, status=status.HTTP_200_OK)
        
        else:return Response({'Error':'No existe ese producto'}, status=status.HTTP_404_NOT_FOUND)
    
    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:return Response({'Error':f'{ID_Producto} no es un entero y debe serlo'}, status=status.HTTP_400_BAD_REQUEST)



from django.db.models import Q

@api_view(['GET'])
def Buscar_producto(request):
    try:
        datos:Dict = request.data
        query = datos['query']

        if datos:
            productos = Producto.objects.filter(Q(producto_nombre__icontains=query))
            pro = ProductoSerializers(productos, many=True)
            return Response(pro.data, status=status.HTTP_200_OK)
            
        else:return Response({'Error':'No se enviaron datos a buscar'}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:return Response({'Error':'Ocurrió un error'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Agregar_Producto_a_Carrito(request):
    try:
        datos:Dict = request.data
        ID_Producto:int = datos['ID_Producto']
        datos_producto = Producto.objects.filter(id=ID_Producto)
        if datos_producto.exists():
            lista_carrito.append(ID_Producto)
            return Response({'Hecho':f'Producto {ID_Producto} agregado al carrito'}, status=status.HTTP_200_OK)
        
        else:return Response({'Error':'No existe ese producto'}, status=status.HTTP_404_NOT_FOUND)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:return Response({'Error':f'{ID_Producto} no es un entero y debe serlo'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def Eliminar_Producto_del_Carrito(request):
    try:
        datos:Dict = request.data
        ID_Producto:int = datos['ID_Producto']
        if ID_Producto in lista_carrito:
            lista_carrito.remove(ID_Producto)
            return Response({'Hecho':f'Se eliminó el producto {ID_Producto} del carrito'}, status=status.HTTP_200_OK)
        
        else:return Response({'Error':f'No existe el producto {ID_Producto} en la lista del carrito'}, status=status.HTTP_204_NO_CONTENT)

    except KeyError as e:return Response({'Error':f'Datos no enviados en {e}'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:return Response({'Error':f'{ID_Producto} no es un entero y debe serlo'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def Obtener_Total_Carrito(request):
    try:
        total:int = 0
        for producto_id in lista_carrito:
            datos = Producto.objects.get(id=producto_id)
            total += datos.producto_precio
        return Response({'Hecho':f'La lista de productos elegidos es {lista_carrito}', 'Carrito' : f'El total del carrito es de {total}'}, status=status.HTTP_200_OK)

    except KeyError as e:return Response({'Error':'Ocurrió un error al procesar el carrito'}, status=status.HTTP_406_NOT_ACCEPTABLE)