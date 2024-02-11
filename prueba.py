import pandas as pd


df = pd.read_csv('youtube_data//youtube_files//yt_ids_check.csv')
print(df['Channel'].value_counts())
