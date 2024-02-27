import BBDD.conexionBBDD.conexionBBDD as conBBDD


def preprocess_silver_scheme(conn_str):
    df_channel = conBBDD.obtener_dataframe('bronze', 'channel', conn_str)
    df_channel = preprocess_channel(df_channel)
    df_channel = df_channel.drop_duplicates(subset='id', keep='first')

    df_video = conBBDD.obtener_dataframe('bronze', 'video', conn_str)
    df_video = preprocess_video(df_video)
    df_video = df_video.drop_duplicates(subset='id', keep='first')

    conBBDD.guardar_df_en_tabla(df_channel, 'channel','silver', conn_str)
    conBBDD.guardar_df_en_tabla(df_video, 'video', 'silver', conn_str)

def preprocess_channel(df_channel):
    df_channel = fill_with_most_repeated_value(df_channel, 'language')
    df_channel = fill_with_most_repeated_value(df_channel, 'country')
    return df_channel


def preprocess_video(df_video):
    df_video = fill_with_most_repeated_value(df_video, 'defaultAudioLanguage')
    df_video = fill_with_0(df_video, 'viewCount')
    df_video = fill_with_0(df_video, 'likeCount')
    df_video = fill_with_0(df_video, 'commentCount')
    df_video['viewCount'] = df_video['viewCount'].astype(int)
    df_video['likeCount'] = df_video['likeCount'].astype(int)
    df_video['commentCount'] = df_video['commentCount'].astype(int)

    df_video['tags'] = df_video['tags'].fillna('[]')

    df_video['liveBroadcastContent'] = df_video['liveBroadcastContent'].replace({'none': 'no', 'upcoming': 'no', 'live': 'yes'})
    df_video['duration'] = df_video['duration'].apply(convert_iso8601_to_seconds)
    df_video['duration'] = df_video['duration'].astype(int)
    df_video['type'] = df_video.apply(classify_content, axis=1)
    df_video = df_video.drop(columns=['liveBroadcastContent'])

    return df_video


def fill_with_0(df, column):
    df[column] = df[column].fillna(0)
    return df

def fill_with_most_repeated_value(df, column):
    most_repeated = df[column].value_counts().idxmax()
    df[column] = df[column].fillna(most_repeated)
    return df

def convert_iso8601_to_seconds(time_str):
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    if 'P' in time_str and 'T' in time_str:
        days_str, time_str = time_str.split('T')
        days_str = days_str[1:] 
        if 'D' in days_str:
            days = int(days_str.split('D')[0])
    else:
        time_str = time_str[2:] 

    if 'H' in time_str:
        hours_str, time_str = time_str.split('H')
        hours = int(hours_str)

    if 'M' in time_str:
        minutes_str, time_str = time_str.split('M')
        minutes = int(minutes_str)

    if 'S' in time_str:
        seconds_str = time_str.split('S')[0]
        seconds = int(seconds_str)

    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return total_seconds


def classify_content(row):
    if row['liveBroadcastContent'] == 'yes':
        return 'live'
    elif row['duration'] < 60:
        return 'short'
    else:
        return 'video'
