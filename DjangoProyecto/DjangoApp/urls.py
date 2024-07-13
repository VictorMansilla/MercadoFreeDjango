from django.urls import path
from .views import Crear_Usuario, Crear_Producto, Obtener_Productos, Obtener_un_Producto, Velidar_Usuario, Actualizar_Usuario, Eliminar_Usuario

urlpatterns = [
    path("api/Usuarios/", Crear_Usuario, name='Crear_Usuario'),
    path("api/Crear_Producto/", Crear_Producto, name='Crear_Producto'),
    path("api/Productos/", Obtener_Productos, name="Obtener_Productos"),
    path("api/Producto/<int:ID_Producto>", Obtener_un_Producto, name="Obtener_un_Producto"),
    path('api/Velidar_Usuario', Velidar_Usuario, name='Velidar_Usuario'),
    path('api/Actualizar_Usuario', Actualizar_Usuario, name='Actualizar_Usuario'),
    path('api/Eliminar_Usuario', Eliminar_Usuario, name='Eliminar_Usuario')
]