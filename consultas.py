import sqlite3

def ejecutar_consultas(path_db='fondos.db'):
    conn = sqlite3.connect(path_db)
    
    # Fondos con mayor número de inversiones en cartera
    consulta_FondosConMasInversiones = '''
    SELECT fondos.nombre, COUNT(cartera.id) AS numero_inversiones
    FROM fondos
    JOIN cartera ON fondos.registro = cartera.registro
    GROUP BY fondos.nombre
    ORDER BY numero_inversiones DESC;
    '''

    # Inversiones con mayor aumento de valor
    consulta_InversionesConMayorAumento = '''
    SELECT descripcion, periodo, 
    ((CAST(importeValorAct AS REAL) - CAST(importeValorAnt AS REAL)) / CAST(importeValorAnt AS REAL)) * 100 AS aumento_porcentaje
    FROM cartera
    WHERE importeValorAnt IS NOT NULL AND importeValorAct IS NOT NULL AND importeValorAnt != '0'
    ORDER BY aumento_porcentaje DESC
    LIMIT 5;
    '''

    # Apuestas más fuertes de cada fondo
    consulta_InversionFuerte = '''
    SELECT fondos.nombre, cartera.descripcion, MAX(cartera.inversionPorcActual) AS PorcentajeActual
    FROM cartera
    JOIN fondos ON cartera.registro = fondos.registro
    GROUP BY fondos.nombre
    ORDER BY PorcentajeActual DESC;
    '''

    # Fondos con mayor capital invertido
    consulta_FondosConMayorCapital = '''
    SELECT fondos.nombre, SUM(cartera.importeValorAct) AS total_invertido
    FROM cartera
    JOIN fondos ON cartera.registro = fondos.registro
    GROUP BY fondos.nombre
    ORDER BY total_invertido DESC;
    '''

    try:
        c = conn.cursor()
        c.execute(consulta_FondosConMasInversiones)
        print("Fondos con Mayor Número de Inversiones en Cartera:")
        for fila in c.fetchall():
            print(f"Fondo: {fila[0]}, Número de Inversiones: {fila[1]}")
        c.close()
        
        c = conn.cursor()
        c.execute(consulta_InversionesConMayorAumento)
        print("\nInversiones con Mayor Aumento de Valor:")
        for fila in c.fetchall():
            print(f"Descripción: {fila[0]}, Periodo: {fila[1]}, Aumento de Valor: {fila[2]:.2f}%")
        c.close()

        c = conn.cursor()
        c.execute(consulta_InversionFuerte)
        print("\nInversiones más Fuertes de Cada Fondo:")
        for fila in c.fetchall():
            print(f"Fondo: {fila[0]}, Inversión: {fila[1]}, Porcentaje Actual: {fila[2]}")
        c.close()

        c = conn.cursor()
        c.execute(consulta_FondosConMayorCapital)
        print("\nFondos con Mayor Capital Invertido:")
        for fila in c.fetchall():
            print(f"Fondo: {fila[0]}, Total Invertido: {fila[1]}")
        c.close()

    except Exception as e:
        print("Ocurrió un error al ejecutar la consulta:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    ejecutar_consultas()