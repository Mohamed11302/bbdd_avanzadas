import os
import requests
import json
import constantes as const
import pandas as pd

def get_api_key():
    return os.getenv("YOUTUBE_CREDENTIAL")

def get_header(api_key):
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    } 

def http_request_yt(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_json = json.loads(response.text)
        return response_json 
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        print(f"Response code: {response.status_code}")
        return None

def check_ids(df, api_key):
    headers = get_header(api_key)
    for i, row in df.iterrows():
        print(i, end=": ")
        params = {
            "part": "id",
            "id": row['ID'],
            "key": api_key
        }
        response_json = http_request_yt(const.YT_API_CHANNELS, params)
        if response_json and response_json.get('pageInfo').get('totalResults') > 0:
            print("OK")
            df.at[i, 'Consulta'] = 1
        else:
            print(f"ERROR: {response_json.status_code}")
            df.at[i, 'Consulta'] = 0
        df.to_csv(const.YT_IDS, index=False)