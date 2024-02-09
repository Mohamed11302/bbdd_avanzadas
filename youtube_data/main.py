import utils
import pandas as pd
import requests
import constantes as const





if __name__ == "__main__":
    credential = utils.get_api_key()
    df = pd.read_csv(const.YT_IDS)
    utils.check_ids(df, credential)

