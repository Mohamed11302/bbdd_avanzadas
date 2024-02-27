import BBDD.conexionBBDD.conexionBBDD as conBBDD
import pandas as pd
import psycopg2
import BBDD.diseno.clases as clases
CREATE_SQL_TABLES_FILE = "BBDD//diseno//gold_tables.sql"

def diseno_gold(conn_str):
    df_video = pd.read_csv('video.csv')
    df_channel= pd.read_csv('channel.csv')

    print("Leidos df_video y df_channel")
    conn=psycopg2.connect(conn_str)
    conn=conn.cursor()
    #drop_tables(conn,"gold")
    #execute_sql_file(conn, CREATE_SQL_TABLES_FILE)
    insert_data2(conn, "gold", df_channel, df_video)
   
    
def insert_data2(conn, schema_name, df_channel, df_video):
    #insert_date(conn, schema_name, df_channel, "creationdate", "id")
    #insert_date(conn, schema_name, df_video, "publishedAt", "id")
    #insert_video_statistics(conn, schema_name, df_video)
    
    #insert_channel_statistics(conn, schema_name, df_channel)    
    #insert_channel(conn, schema_name, df_channel)
    #insert_fact_channelstats(conn, schema_name, df_channel)
    
    insert_video(conn, schema_name, df_video) #AÑADIR INSERTAR TAGS
    #insert_fact_videostats(conn, schema_name, df_video)


def insert_fact_channelstats(conn, schema_name, df):
    for index, row in df.iterrows():
      print(index)
      try:
        channel_facts = clases.create_channel_facts_from_csv(row)
        insert_fact_channelstats_query = f"""
        INSERT INTO {schema_name}.fact_channelstats (stats_id, date_id, channel_id)
        VALUES (%s, %s, %s);
        """
        conn.execute(insert_fact_channelstats_query, (channel_facts.stats_id, channel_facts.dates, channel_facts.channel))
      except Exception as e:
        print(f"Error al insertar las estadísticas del canal {channel_facts.stats_id}: {e}")
        break
    conn.connection.commit()


def insert_fact_videostats(conn, schema_name, df):
    for index, row in df.iterrows():
      print(index)
      try:
        video_facts = clases.create_video_facts_from_csv(row)
        insert_fact_videostats_query = f"""
        INSERT INTO {schema_name}.fact_videostats (stats_id, date_id, video_id, channel_id)
        VALUES (%s, %s, %s, %s);
        """
        conn.execute(insert_fact_videostats_query, (video_facts.stats_id, video_facts.dates, video_facts.video, video_facts.channel))
      except Exception as e:
        print(f"Error al insertar las estadísticas del video {video_facts.stats_id}: {e}")
        break
    conn.connection.commit()


def insert_channel(conn, schema_name, df):
    for index, row in df.iterrows():
      print(index)
      channel = clases.create_channel_from_csv(row)
      try:
        insert_channel_query = f"""
        INSERT INTO {schema_name}.channel (channel_id, name, statistics_id, language, country)
        VALUES (%s, %s, %s, %s, %s);
        """
        conn.execute(insert_channel_query, (channel.channel_id, channel.name, channel.statistics_id, channel.language, channel.country))
      except Exception as e:
        print(f"Error al insertar el canal {channel.channel_id}: {e}")
        break
    conn.connection.commit()


def insert_video(conn, schema_name, df):
    for index, row in df.iterrows():
      print(index)
      video = clases.create_video_from_csv(row)
      try:
          insert_video_query = f"""
          INSERT INTO {schema_name}.video (video_id, title, statistics_id, category_id, duration, default_audio_language, type)
          VALUES (%s, %s, %s, %s, %s, %s, %s);
          """
          conn.execute(insert_video_query, (video.video_id, video.title, video.statistics_id, video.category_id, video.duration, video.default_audio_language, video.type))
      except Exception as e:
          print(f"Error al insertar el video {video.video_id}: {e}")
    conn.connection.commit()

def insert_video_statistics(conn, schema_name, df):
    for index, row in df.iterrows():
      print(index)
      video_stats = clases.create_video_statistics_from_csv(row)
      try:
        insert_channel_stats_query = f"""
        INSERT INTO {schema_name}.videostatistics(stats_id, view_count, like_count, comment_count)
        VALUES (%s, %s, %s, %s);
        """
        conn.execute(insert_channel_stats_query, (video_stats.stats_id,  video_stats.view_count, video_stats.like_count, video_stats.comment_count))
      except Exception as e:
        print(f"Error al insertar las estadísticas del canal {video_stats.stats_id}: {e}")
        break
    conn.connection.commit()

def insert_channel_statistics(conn, schema_name, df):
  REDONDEO = 1000
  for index, row in df.iterrows():
    print(index)
    channel_stats = clases.create_channel_statistics_from_csv(row)
    try:
      insert_channel_stats_query = f"""
      INSERT INTO {schema_name}.channelstatistics (stats_id, subscribers, view_count, num_videos)
      VALUES (%s, %s, %s, %s);
      """
      conn.execute(insert_channel_stats_query, (channel_stats.stats_id,  channel_stats.subscribers, channel_stats.view_count/REDONDEO, channel_stats.num_videos))
    except Exception as e:
        print(f"Error al insertar las estadísticas del canal {channel_stats.stats_id}: {e}")
        break
  conn.connection.commit()

def insert_date(conn, schema_name, df, column_date, column_identifier):
  for index, row in df.iterrows():
    print(index)
    date = clases.create_date_from_csv(row, df, column_date, column_identifier)
    try:
        insert_date_query = f"""
        INSERT INTO {schema_name}.dates (date_id, year, month, day, hour, min, sec)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        conn.execute(insert_date_query, (date.date_id, date.year, date.month, date.day, date.hour, date.min, date.sec))
    except Exception as e:
        print(f"Error al insertar la fecha {date.date_id}: {e}")
  conn.connection.commit()


def execute_sql_file(cursor, sql_file_path):
    with open(sql_file_path, 'r') as sql_file:
        sql_commands = sql_file.read()
    try:
      cursor.execute(sql_commands)
      cursor.connection.commit()
      print(f"Fichero sql {sql_file_path} ejecutado correctamente")
    except Exception as e:
        print(f"Something went wrong: {e}") 


def drop_tables(conn,schema_name):
        tables = [
            "dates",
            "video",
            "channel",
            "videostatistics",
            "channelstatistics",
            "videostats",
            "channelstats",
            "tag"
        ]

        for table in tables:
            try:
                conn.execute(f"DROP TABLE IF EXISTS {schema_name}.{table} CASCADE;")
                conn.connection.commit()
                print(f"Tabla {table} eliminada correctamente")
            except psycopg2.Error as e:
                print(f"Error al eliminar la tabla {table}: {e}")
