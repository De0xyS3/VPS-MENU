import os
import requests

# Solicitar el token
token = input('Enter the token: ')

# Validar el token con el servidor B
response = requests.post('http://servidor_b.com/validate_token', json={'token': token})

if response.status_code == 200:
    # Ejecutar la serie de instrucciones
    # ...
else:
    # Borrar el script
    os.remove(__file__)
    print('Token invalid, script deleted.')
