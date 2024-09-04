# MercadoFreeDjango

MercadoFreeDjango es una implementación de un backend inspirado en Mercado Libre, desarrollado en Django. Este proyecto incluye manejo de usuarios y productos, consultas seguras a la base de datos, revocación de tokens JWT, protección de variables de entorno, y una funcionalidad de búsqueda de productos.

# Características

CRUD de Usuarios y Productos: Gestión completa de creación, lectura, actualización y eliminación.
Registro de Actividades: Registro de acciones realizadas en la plataforma para usuarios y productos.
Consultas Seguras: Uso de un ORM para realizar consultas a la base de datos, previniendo inyecciones SQL.
Variables de Entorno: Uso de dotenv para proteger y manejar de manera segura las variables sensibles.
Autenticación: Implementación de JWT para la autenticación segura de usuarios.
Revocación de Tokens JWT: Integración con Redis para manejar la revocación de tokens y el deslogueo de usuarios.
Manejo de Excepciones: Gestión de errores robusta para mejorar la experiencia del usuario.
Scripts para Linux: Uso de archivos .sh para automatizar tareas en sistemas Linux.

# Tecnologías usadas

- Python 3.10.3
- Django 5.0.6
- PostgreSQL 16
- Redis 6.2.14
- JWT 2.8.0
- Bcrypt 4.1.3
- Dotenv 1.0.1
- Render para el despliuegue de la aplicación

# Enlace general de la aplicación

URL: https://mercadofreedjango.onrender.com/

# ENDPOINTS y formatos JSON

CREACIÓN DE USUARIOS (POST)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Crear_Usuario/

JSON ejemplo: 

{
    "nombre_usuario" : "Aquí va el nombre del usuario (campo obligatorio)",
    "contrasegna_usuario" : "Aquí va la contraseña del usuario (campo obligatorio)",
    "email_usuario" : "Aquí va el email del usuario (campo opcional, por default será NULL)",
    "telefono_usuario" : "Aquí va el teléfono del usuario (campo obligatorio por default será NULL)"
}

###########################################################################################################################################################

LOGIN DE USUARIOS (GET)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Validar_Usuario/

JSON ejemplo: 

{
    "nombre_usuario" : "Aquí va el nombre del usuario ya creado (campo obligatorio)",
    "contrasegna_usuario" : "Aquí va la contraseña del usuario ya creado (campo obligatorio)"
}

y devuelve este formato json:

{
    "Login exitoso": "Contraseña válida",
    "token": "token jwt"
}

El token contiene el id del usuario, el nombre del usuario y la expiración del usuario en 2000 segundos

###########################################################################################################################################################

LOGOUT DE USUARIOS (POST)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Desvalidar_Usuario/

JSON ejemplo:

{
    "token" : "Aquí va el token, obligatorio, de ahí se sacará la id (campo obligatorio)"
}

###########################################################################################################################################################

ACTUALIZACIÓN DE DATOS DEL USUARIO (PUT)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Actualizar_Usuario/

JSON ejemplo:

{
    "contrasegna_usuario" : "Aquí va la contraseña del usuario para que pueda acceder a editar sus datos (campo obligatorio)",
    "nuevo_nombre_usuario" : "Aquí a el nuevo nombre del usuario (campo opcional, por defecto se pondrá el nombre que ya tiene)",
    "nueva_contrasegna_usuario" : "Aquí va la nueva contraseña del usuario (campo obligatorio)",
    "nuevo_email_usuario" : "Aquí va el nuevo email del usuario (campo opcional, por defecto se pondrá el email que ya tiene)",
    "nuevo_telefono_usuario" : "Auí va el nuevo teléfono del usuario (campo opciona, por defecto se pondrá el teléfono que ya tiene)",
    "token" : "Aquí va el token, obligatorio, de ahí se sacará la id (campo obligatorio)"
}

###########################################################################################################################################################

ELIMINACIÓN DEL USUARIO (DELETE)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Eliminar_Usuario/

JSON ejemplo:

{
    "contrasegna_usuario" : "Aquí va la contraseña del usuario (campo obligatorio)",
    "token" : "Aquí va el token, obligatorio, de ahí se sacará la id (campo obligatorio)"
}

###########################################################################################################################################################

CREACIÓN DE PRODUCTO (POST)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Crear_Producto/

JSON ejemplo:

{
    "producto_nombre" : "Aquí va el nombre del producto (campo obligatorio)",
    "producto_precio" : Aquí va el precio del producto, ustedes se aseguran que sea formato int (campo obligatorio),
    "producto_descripcion" : "Aquí va la descripción del producto (campo opcional, por defecto se pondrá un NULL)",
    "token" : "Aquí va el token, obligatorio para saber que usuario creo el producto (campo obligatorio)"
}

###########################################################################################################################################################

ACTUALIZACIÓN DE DATOS DEL USUARIO (PUT)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Editar_Producto/

JSON ejemplo:

{
    "id_producto" : "Aquí va la id del producto a editar valores (campo obligatorio)",
    "nuevo_producto_nombre" : "Aquí va el nombre del producto (campo obligatorio)",
    "nuevo_producto_precio" : Aquí va el nuevo precio del producto, ustedes se aseguran que sea formato int (campo obligatorio),
    "nueva_producto_descripcion" : "Aquí va la nueva descripción del producto (campo obligatorio, por defecto se pondrá el valor que ya tiene)",
    "token" : "Aquí va el token (campo obligatorio)"
}

###########################################################################################################################################################

ELIMINACIÓN DEL PRODUCTO (DELETE)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Eliminar_Producto/

JSON ejemplo:

{
    "id_producto" : "Aquí va la id del producto a eliminar (campo obligatorio)",
    "token" : "Aquí va el token (campo obligatorio)"
}

###########################################################################################################################################################

OBTENCIÓN DE TODOS LOS PRODUCTOS (GET)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Productos/

###########################################################################################################################################################

OBTENCIÓN DE UN PRODUCTO ESPECÍFICO (GET)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Producto/int

En <int> agregan la id del producto a buscar

###########################################################################################################################################################

OBTENCIÓN DE TODOS LOS PRODUCTOS POR BÚSQUEDA (GET)

URL: https://mercadofreedjango.onrender.com/DjangoApp/Buscar_producto/

JSON ejemplo:

{
    "query" : "Aquí va el nombre del producto a buscar (campo obligatorio)"
}

