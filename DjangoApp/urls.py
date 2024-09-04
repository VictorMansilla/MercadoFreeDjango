from django.urls import path
from .views import Crear_Usuario, Validar_Usuario, Desvalidar_Usuario, Actualizar_Usuario, Eliminar_Usuario, Crear_Producto, Editar_Producto, Eliminar_Producto, Obtener_Productos, Obtener_un_Producto, Buscar_producto, Agregar_Producto_a_Carrito, Eliminar_Producto_del_Carrito, Obtener_Total_Carrito
from .payment import Paypal

urlpatterns = [
    path("Crear_Usuario/", Crear_Usuario, name='Crear_Usuario'),
    path('Validar_Usuario/', Validar_Usuario, name='Validar_Usuario'),
    path('Actualizar_Usuario/', Actualizar_Usuario, name='Actualizar_Usuario'),
    path('Eliminar_Usuario/', Eliminar_Usuario, name='Eliminar_Usuario'),
    
    path('Desvalidar_Usuario/', Desvalidar_Usuario, name='Desvalidar_Usuario'),
    
    path("Crear_Producto/", Crear_Producto, name='Crear_Producto'),
    path("Editar_Producto/", Editar_Producto, name='Editar_Producto'),
    path("Eliminar_Producto/", Eliminar_Producto, name='Eliminar_Producto'),

    path("Paypal/", Paypal, name="Paypal"),
    
    path("Productos/", Obtener_Productos, name="Obtener_Productos"),
    path("Producto/<ID_Producto>", Obtener_un_Producto, name="Obtener_un_Producto"),
    path("Buscar_producto/", Buscar_producto, name="Buscar_producto"),
    path("Agregar_Producto_a_Carrito/", Agregar_Producto_a_Carrito, name="Agregar_Producto_a_Carrito"),
    path("Eliminar_Producto_del_Carrito/", Eliminar_Producto_del_Carrito, name="Eliminar_Producto_del_Carrito"),
    path("Obtener_Total_Carrito/", Obtener_Total_Carrito, name="Obtener_Total_Carrito"),
]