import os
import datetime
import jwt

segundos_exp = int(os.getenv('segundos_exp'))
clave_secreta = os.getenv('clave_secreta')   #secrets.token_hex(62)
algoritmo:list = [os.getenv('algoritmo')]

def Generar_Token(nombre_usuario_token, id_usuario_token):
    payload = {
        'Id_usuario' : id_usuario_token,
        'nombre_usuario' : nombre_usuario_token,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=segundos_exp)}
    token = jwt.encode(payload, clave_secreta, algorithm=os.getenv('algoritmo'))
    return token



def Deployar_Token(token):
    try:
        token_payload:str = jwt.decode(token, os.getenv('clave_secreta'), os.getenv('algoritmo'))
        return token_payload
        
    except jwt.DecodeError:raise jwt.DecodeError('Error al decodificar el token')

    except jwt.ExpiredSignatureError: raise jwt.ExpiredSignatureError('El token a expirado')

    except jwt.InvalidTokenError: raise jwt.InvalidTokenError('Error en la validación del token')