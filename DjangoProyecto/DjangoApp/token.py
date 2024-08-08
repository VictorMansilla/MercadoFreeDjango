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