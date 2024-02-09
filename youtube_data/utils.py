import os
import requests
import json
import constantes as const
import pandas as pd
def get_api_key():
    return os.getenv(const.YT_APIKEY)


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

def check_ids_aux(df, api_key):
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
        df.to_csv(const.YT_IDS_CHECK, index=False)
    return df

def check_ids(api_key):
    df = pd.read_csv(const.YT_IDS_UNCHECK)
    df = check_ids_aux(df, api_key)
    return df

