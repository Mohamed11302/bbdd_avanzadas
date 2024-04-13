import sqlite3

def crear_bbdd(path_db='fondos.db'):
    conn = sqlite3.connect(path_db)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS fondos (
            registro INTEGER PRIMARY KEY,
            nombre TEXT,
            correo TEXT,
            direccion TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS cartera (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            inversionPorcActual TEXT,
            inversionPorcAnterior TEXT,
            importeValorAct TEXT,
            importeValorAnt TEXT,
            periodo TEXT,
            registro INTEGER,
            FOREIGN KEY (registro) REFERENCES fondos(registro)
            UNIQUE(descripcion, periodo)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_bbdd()