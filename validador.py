from flask import Flask, request
import time

app = Flask(__name__)

# Diccionario para aslmacenar los tokens
tokens = {}

# Endpoint que recibe el token
@app.route('/receive_token', methods=['POST'])
def receive_token():
  # Recibir el token del servidor A
  token = request.json.get('token')
  if token:
    # Almacenar el token
    tokens[token] = int(time.time()) + 2 * 60 * 60 # 2 horas
    return 'Token almacenado.', 200
  else:
    return 'No se ha enviado un token válido.', 400

# Endpoint que valida el token
@app.route('/validate_token', methods=['POST'])
def validate_token():
  # Recibir el token a validar
  token = request.json.get('token')
  if token in tokens:
    # Verificar si el token aún es válido
    if int(time.time()) < tokens[token]:
      return 'Token válido.', 200
    else:
      # Eliminar el token si ya ha expirado
      del tokens[token]
      return 'Token inválido.', 400
  else:
    return 'Token no encontrado.', 400

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8000, debug=True)
#  app.run(port=8000, debug=true)