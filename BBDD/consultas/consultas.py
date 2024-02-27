import BBDD.conexionBBDD.conexionBBDD as conBBDD
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime

BASE_DIRECTORY = 'BBDD//consultas//'

def consultas():
    conn_str = conBBDD.get_bbdd_url()
    print("Ejecutando consultas")
    conn=psycopg2.connect(conn_str)
    conn=conn.cursor()
    consulta_1(conn, BASE_DIRECTORY + "consulta_1.sql")
    consulta_2(conn, BASE_DIRECTORY + "consulta_2.sql")
    consulta_3(conn, BASE_DIRECTORY + "consulta_3.sql")


def consulta_1(conn, sql_file_path):
    data = execute_sql_file(conn, sql_file_path)
    plot_consulta_1(data)

def consulta_2(conn, sql_file_path):
    data = execute_sql_file(conn, sql_file_path)
    fetch_top_videos(data)


def consulta_3(conn, sql_file_path):
    data = execute_sql_file(conn, sql_file_path)
    plot_consulta_3(data)

def plot_consulta_3(data):
    category_map = {
        2: 'Autos\n&\nVehicles',
        1: 'Film\n&\nAnimation',
        10: 'Music',
        15: 'Pets\n&\nAnimals',
        17: 'Sports',
        18: 'Short\nMovies',
        19: 'Travel\n&\nEvents',
        20: 'Gaming',
        21: 'Videoblogging',
        22: 'People\n&\nBlogs',
        23: 'Comedy',
        24: 'Entertain-\nment',
        25: 'News\n&\nPolitics',
        26: 'Howto\n&\nStyle',
        27: 'Education',
        28: 'Science\n&\nTechnology',
        29: 'Nonprofits\n&\nActivism'
    }

    # Traducir categorías y ordenar datos
    df = pd.DataFrame(data, columns=['category_id', 'total_views'])
    df['category_name'] = df['category_id'].map(category_map)    

    # Crear gráfico de barras
    plt.bar(df['category_name'], df['total_views'], color='skyblue')
    plt.ylabel(r'$\mathbf{Total\ Views}$')
    plt.xlabel(r'$\mathbf{Category\ Name}$')
    plt.title('Total Views by Category')
    plt.show()



def fetch_top_videos(data):
    print(f'{"Channel Name":<30} {"Subscribers":<12} {"Video Title":<98} {"VideoType":<10} {"VideoViews":<12}')
    print('-'*200)
    for row in data:
        print(f'{row[0]:<30} {row[1]:<12} {row[2]:<100} {row[3]:<8} {row[4]:<12}')





def convertir_a_lista(ruta_del_archivo):
    with open(ruta_del_archivo, 'r') as archivo:
        datos = archivo.read()
        lista = eval(datos)
    return lista


def plot_consulta_1(data):
    # Filtrar datos para obtener solo los de 2023 y 2024, excluyendo los meses desde marzo de 2024 hasta diciembre de 2024
    data_2023_2024 = [(ano, mes, tipo, num_videos) for ano, mes, tipo, num_videos in data if (2023 <= ano <= 2024) and not (ano == 2024 and 3 <= mes <= 12)]

    # Obtener tipos de video únicos
    tipos_de_video = set(tipo for _, _, tipo, _ in data_2023_2024)

    # Crear diccionario para almacenar datos de 2023 y 2024 por tipo y por mes
    data_dict = {tipo: {f"{ano}-{mes}": 0 for ano in range(2023, 2025) for mes in range(1, 13) if not (ano == 2024 and 3 <= mes <= 12)} for tipo in tipos_de_video}

    # Llenar diccionario con datos de 2023 y 2024
    for ano, mes, tipo, num_videos in data_2023_2024:
        data_dict[tipo][f"{ano}-{mes}"] += num_videos

    # Obtener tipos de video y meses
    tipos_de_video = list(data_dict.keys())
    tipos_de_video = sorted(tipos_de_video, key=lambda x: ['video', 'short', 'live'].index(x))
    meses = sorted(list(data_dict[tipos_de_video[0]].keys()), key=lambda x: datetime.strptime(x, "%Y-%m"))

    # Configurar el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))

    # Crear las barras para cada tipo de video
    bottom = np.zeros(len(meses))
    for i, tipo in enumerate(tipos_de_video):
        num_videos = [data_dict[tipo][mes] for mes in meses]
        bars = ax.bar(np.arange(len(meses)), num_videos, bottom=bottom, label=tipo)
        bottom += num_videos
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2,
                int(height), ha='center', va='center')

    # Configurar las etiquetas del eje x
    ax.set_xticks(np.arange(len(meses)))
    ax.set_xticklabels(meses)

    # Configurar las etiquetas y título del gráfico
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Videos')
    ax.set_title('Number of Videos by Type and Month')
    ax.legend()

    # Mostrar el gráfico
    plt.show()

def execute_sql_file(cursor, sql_file_path):
    with open(sql_file_path, 'r') as sql_file:
        sql_commands = sql_file.read()
    try:
      cursor.execute(sql_commands)
      print(f"Fichero sql {sql_file_path} ejecutado correctamente")
    except Exception as e:
        print(f"Something went wrong: {e}") 
    return cursor.fetchall()