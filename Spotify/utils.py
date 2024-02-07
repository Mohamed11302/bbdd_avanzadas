import requests
import json
import os
import Constantes as Const
import time
def get_id_and_secrets():
    client_id = os.getenv(Const.ENV_CLIENT_ID)
    client_secret = os.getenv(Const.ENV_CLIENT_SECRET)
    if client_id == None:
        print(f"Configura la variable de entorno de {Const.ENV_CLIENT_ID}")
        raise SystemExit(0)
    if client_secret == None:
        print(f"Configura la variable de entorno de {Const.ENV_CLIENT_SECRET}")
        raise SystemExit(0)
    return client_id, client_secret


def get_token(client_id, client_secret):
    url = Const.SPOTIFY_TOKEN_URL
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Lanza una excepción para códigos de respuesta HTTP distintos de 2xx
        token = response.json()["access_token"]
        return token
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        print(f"Response code: {response.status_code}")
        raise SystemExit(0)

    
def http_request(url, headers, params):
    try:
        response = requests.get(url, headers=headers, params=params)
        
        while response.status_code == 429: #Muchas peticiones, esperamos un poco
            print("Muchas peticiones, esperamos 30 segundos")
            print(response.headers['retry-after'])
            time.sleep(30)  
            print("Continuacion del programa")
            response = requests.get(url, headers=headers, params=params)            

        response.raise_for_status()  # Lanza una excepción para códigos de respuesta HTTP distintos de 2xx

        response_json = json.loads(response.text)
        return response_json
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        print(f"Response code: {response.status_code}")
        raise SystemExit(0)
