from datetime import datetime
import conexionBBDD.conexionBBDD as conBBDD
import pandas as pd
import psycopg2

def diseno_gold(conn_str):
    df_video = pd.read_csv('video.csv')
    df_channel= pd.read_csv('channel.csv')

    print("Leidos df_video y df_channel")
    conn=psycopg2.connect(conn_str)
    conn=conn.cursor()
    #create_table_example(conn,"gold", "prueba", "employee_id SERIAL PRIMARY KEY,first_name VARCHAR(50),last_name VARCHAR(50),birth_date DATE,joined_date TIMESTAMP,department VARCHAR(50)")
    #drop_tables(conn,"gold")
    create_tables(conn,"gold")
    conn.connection.commit()
    insert_data(conn, "gold",df_video, df_channel)
    conn.connection.commit()
    print("Datos insertados")
    establish_relationships(conn,"gold")
    conn.connection.commit()
    print("Tablas conectadas")

def create_table_example(conn, schema_name, table_name, attributes):
    try:
        # Create schema if it doesn't exist
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
        
        # Create table
        query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
            {attributes}
        );
        """
        conn.execute(query)
        print(f"Table {table_name} created successfully in schema {schema_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_tables(conn, schema_name):
  
  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.dates (
      date_id VARCHAR(255) PRIMARY KEY,
      year INT NOT NULL,
      month INT NOT NULL,
      day INT NOT NULL,
      hour INT NOT NULL,
      min INT NOT NULL,
      sec INT NOT NULL
    )
  """
  try:
    conn.execute(create_table_query)
    print("Tabla 'dates' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'dates': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.Video (
      video_id VARCHAR(255) PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      statistics_id VARCHAR(255) NOT NULL,
      category_id INT NOT NULL,
      duration VARCHAR(255) NOT NULL,
      default_audio_language VARCHAR(255) NOT NULL,
      type VARCHAR(255) NOT NULL
    )
  """
  try:
    conn.execute(create_table_query)
    print("Tabla 'Video' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'Video': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.Channel (
        channel_id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        statistics_id VARCHAR(255) NOT NULL,
        language VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL
        )
  """
  try:
    conn.execute(create_table_query)
    print("Tabla 'Channel' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'Channel': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.VideoStatistics (
        stats_id VARCHAR(255) PRIMARY KEY,
        view_count INT NOT NULL,
        like_count INT NOT NULL,
        comment_count INT NOT NULL
        )
    """
  try:
    conn.execute(create_table_query)
    print("Tabla 'VideoStatistics' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'VideoStatistics': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.ChannelStatistics (
        stats_id VARCHAR(255) PRIMARY KEY,
        subscribers INT NOT NULL,
        view_count INT NOT NULL,
        num_videos INT NOT NULL
        )
    """
  try:
    conn.execute(create_table_query)
    print("Tabla 'ChannelStatistics' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'ChannelStatistics': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.VideoStats (
        stats_id VARCHAR(255) PRIMARY KEY,
        date_id VARCHAR(255) NOT NULL,
        video_id VARCHAR(255) NOT NULL,
        channel_id VARCHAR(255) NOT NULL
        )
  """
  try:
    conn.execute(create_table_query)
    print("Tabla 'VideoStats' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'VideoStats': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.ChannelStats (
        stats_id VARCHAR(255) PRIMARY KEY,
        date_id VARCHAR(255) NOT NULL,
        channel_id VARCHAR(255) NOT NULL
        )
  """
  try:
    conn.execute(create_table_query)
    print("Tabla 'ChannelStats' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'ChannelStats': {e}")

  create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.Tag (
        tag_id SERIAL PRIMARY KEY,
        tag_name VARCHAR(255) NOT NULL
        )
    """
  try:
    conn.execute(create_table_query)
    print("Tabla 'Tag' creada correctamente")
  except Exception as e:
    print(f"Error al crear la tabla 'Tag': {e}")

def insert_data(conn, schema_name ,df_video, df_channel):
  
  for row in df_video.itertuples():
    dates = create_date_from_csv(row, df_video)
    try:
      insert_date_query = f"""
        INSERT INTO {schema_name}.dates (date_id, year, month, day, hour, min, sec)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
      """
      conn.execute(insert_date_query, (dates.date_id, dates.year, dates.month, dates.day, dates.hour, dates.min, dates.sec))

    except psycopg2.IntegrityError as e:
      update_date_query = f"""
        WITH ranked_dates AS (
          SELECT 
            date_id,
            ROW_NUMBER() OVER (PARTITION BY date_id ORDER BY ctid) AS rn
          FROM 
            {schema_name}.dates
        )
        UPDATE {schema_name}.dates AS d
        SET date_id = CONCAT(d.date_id, '_' , r.rn)
        FROM ranked_dates AS r
        WHERE d.date_id = r.date_id;
      """
      conn.execute(update_date_query, (dates.year, dates.month, dates.day, dates.hour, dates.min, dates.sec, dates.date_id))

  for row in df_video.itertuples():
    video = create_video_from_csv(row, df_video)
    insert_video_query = f"""
      INSERT INTO {schema_name}.Video (video_id, title, statistics_id, category_id, duration, default_audio_language, type)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn.execute(insert_video_query, (video.video_id, video.title, video.statistics_id, video.category_id, video.duration, video.default_audio_language, video.type))

  for row in df_channel.itertuples():
    channel = create_channel_from_csv(row, df_channel)
    insert_channel_query = f"""
      INSERT INTO {schema_name}.Channel (channel_id, name, statistics_id, language, country)
      VALUES (%s, %s, %s, %s, %s)
    """
    conn.execute(insert_channel_query, (channel.channel_id, channel.name, channel.statistics_id, channel.language, channel.country))

  for row in df_video.itertuples():
    video_stats = create_video_stats_from_csv(row, video, channel, dates)
    insert_video_stats_query = f"""
      INSERT INTO {schema_name}.VideoStats (stats_id, date_id, video_id, channel_id)
      VALUES (%s, %s, %s, %s)
    """
    conn.execute(insert_video_stats_query, (video_stats.stats_id, video_stats.dates.date_id, video_stats.video.video_id, video_stats.channel.channel_id))

  for row in df_channel.itertuples():
    channel_stats = create_channel_stats_from_csv(row, channel, dates)
    insert_channel_stats_query = f"""
      INSERT INTO {schema_name}.ChannelStats (stats_id, date_id, channel_id)
      VALUES (%s, %s, %s)
    """
    conn.execute(insert_channel_stats_query, (channel_stats.stats_id, channel_stats.dates.date_id, channel_stats.channel.channel_id))

# Funciones para crear instancias a partir de los datos CSV
def create_date_from_csv(row, df_video):
    date_time_obj = datetime.strptime(row[4], '%Y-%m-%dT%H:%M:%SZ')
    date_id = row[4]
    return dates(date_id, date_time_obj.year, date_time_obj.month, date_time_obj.day, date_time_obj.hour, date_time_obj.minute, date_time_obj.second)

def create_video_from_csv(row):
    tags = row['tags'].strip("[]").split(", ")
    return Video(row['id'], row['title'], row['id'], row['categoryId'], row['duration'], row['defaultAudioLanguage'], row['type'], tags)

def create_channel_from_csv(row):
    return Channel(row['id'], row['name'], row['id'], row['language'], row['country'])

def create_video_statistics_from_csv(row):
    return VideoStatistics(row['id'], row['viewCount'], row['likeCount'], row['commentCount'])

def create_channel_statistics_from_csv(row):
    return ChannelStatistics(row['id'], row['subscribers'], row['viewcount'], row['numvideos'])

def create_video_stats_from_csv(row, video, channel, dates):
    return VideoStats(row['id'], dates, video, channel)

def create_channel_stats_from_csv(row, channel, dates):
    return ChannelStats(row['id'], dates, channel)


def establish_relationships(conn, schema_name):

    # Establecer la relación entre "VideoStats" y "Video"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.Video
    ADD FOREIGN KEY (statistics_id) REFERENCES VideoStatistics(stats_id)
    """
    conn.execute(alter_table_query)

    # Establecer la relación entre "ChannelStats" y "Channel"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.Channel
    ADD FOREIGN KEY (statistics_id) REFERENCES ChannelStatistics(stats_id)
    """
    conn.execute(alter_table_query)

    # Establecer la relación entre "VideoStats" y "Date"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.VideoStats
    ADD FOREIGN KEY (date_id) REFERENCES dates(date_id)
    """
    conn.execute(alter_table_query)

    # Establecer la relación entre "VideoStats" y "Video"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.VideoStats
    ADD FOREIGN KEY (video_id) REFERENCES Video(video_id)
    """
    conn.execute(alter_table_query)

    # Establecer la relación entre "VideoStats" y "Channel"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.VideoStats
    ADD FOREIGN KEY (channel_id) REFERENCES Channel(channel_id)
    """
    conn.execute(alter_table_query)

    # Establecer la relación entre "ChannelStats" y "Date"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.ChannelStats
    ADD FOREIGN KEY (date_id) REFERENCES dates(date_id)
    """
    conn.execute(alter_table_query)

    # Establecer la relación entre "ChannelStats" y "Channel"
    alter_table_query = f"""
    ALTER TABLE {schema_name}.ChannelStats
    ADD FOREIGN KEY (channel_id) REFERENCES Channel(channel_id)
    """
    conn.execute(alter_table_query)

    alter_table_query = f"""
    ALTER TABLE {schema_name}.Tag
    ADD FOREIGN KEY (video_id) REFERENCES Video(video_id)
    """
    conn.execute(alter_table_query)

# Clases para representar las tablas de la base de datos

class dates:
    def __init__(self, date_id, year, month, day, hour, min, sec):
        self.date_id = date_id
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec

class Video:
    def __init__(self, video_id, title, statistics_id, category_id, duration, default_audio_language, type, tags=[]):
        self.video_id = video_id
        self.title = title
        self.statistics_id = statistics_id
        self.category_id = category_id
        self.duration = duration
        self.default_audio_language = default_audio_language
        self.type = type
        self.tags = tags

class Channel:
    def __init__(self, channel_id, name, statistics_id, language, country):
        self.channel_id = channel_id
        self.name = name
        self.statistics_id = statistics_id
        self.language = language
        self.country = country
    
class VideoStatistics:
    def __init__(self, stats_id, view_count, like_count, comment_count):
        self.stats_id = stats_id
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count

class ChannelStatistics:
    def __init__(self, stats_id, subscribers, view_count, num_videos):
        self.stats_id = stats_id
        self.subscribers = subscribers
        self.view_count = view_count
        self.num_videos = num_videos

class VideoStats:
    def __init__(self, stats_id, dates, video, channel):
        self.stats_id = stats_id
        self.dates = dates
        self.video = video
        self.channel = channel

class ChannelStats:
    def __init__(self, stats_id, dates, channel):
        self.stats_id = stats_id
        self.dates = dates
        self.channel = channel

    def get_stats_id(self):
        return self.stats_id

    def get_date(self):
        return self.dates

    def get_channel(self):
        return self.channel

    def set_stats_id(self, stats_id):
        self.stats_id = stats_id

    def set_date(self, dates):
        self.dates = dates

    def set_channel(self, channel):
        self.channel = channel


def drop_tables(conn,schema_name):

        tables = [
            "date",
            "dates",
            "Video",
            "Channel",
            "VideoStatistics",
            "ChannelStatistics",
            "VideoStats",
            "ChannelStats",
            "Tag"
        ]

        for table in tables:
            try:
                conn.execute(f"DROP TABLE IF EXISTS {schema_name}.{table} CASCADE;")
                print(f"Tabla {table} eliminada correctamente")
            except psycopg2.Error as e:
                print(f"Error al eliminar la tabla {table}: {e}")
