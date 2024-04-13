import sqlite3
from extraer_datos2 import obtener_datos

def insertar_datos(path_db):
    fondos_data, carteras_data = obtener_datos()
    conn = sqlite3.connect(path_db)
    c = conn.cursor()

    for fondo in fondos_data:
        c.execute('''
            INSERT OR IGNORE INTO fondos (registro, nombre, correo, direccion)
            VALUES (?, ?, ?, ?)
        ''', (fondo['registro'], fondo['identifier'], fondo['correo'], fondo['direccion']))

    for cartera in carteras_data:
        c.execute('''
            INSERT OR IGNORE INTO cartera (descripcion, registro, periodo, importeValorAct, importeValorAnt, inversionPorcActual, inversionPorcAnterior)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (descripcion, periodo) DO UPDATE SET
            registro = excluded.registro,
            importeValorAct = excluded.importeValorAct,
            importeValorAnt = excluded.importeValorAnt,
            inversionPorcActual = excluded.inversionPorcActual,
            inversionPorcAnterior = excluded.inversionPorcAnterior
        ''', (
            cartera['descripcion'], cartera['registro'], cartera['periodo'],
            cartera.get('importeValorAct', ''), cartera.get('importeValorAnt', ''),
            cartera.get('inversionPorcActual', ''), cartera.get('inversionPorcAnterior', '')
        ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    path_db = 'fondos.db'
    insertar_datos(path_db)