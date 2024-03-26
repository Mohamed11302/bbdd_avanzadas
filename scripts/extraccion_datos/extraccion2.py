import xml.etree.ElementTree as ET
import os

RUTA_MOHAMED = 'C:\\Users\\mohae\\Desktop\\2º Semestre\\BBDD Avanzadas\\Bloques\\Bloque 2 Xml\\Trabajo\\Trabajo 1\\FullOct2007.xml'
CATEGORIAS_DESEADAS = ['Video & Online Games', 'Music & Music Players', 'Reality Television', 'Other - Entertainment']
RUTA_DESTINO = 'files/categorias_filtradas.xml'

def filtrar_categorias(file_name, categorias_deseadas, output_file):
    print("Comenzando a filtrar...")
    i = 0
    # Estimación del número total de documentos basada en el tamaño del archivo
    total_docs_estimado = os.path.getsize(file_name) / 1000  # Ajusta el divisor según tus datos
    with open(output_file, 'wb') as output:
        output.write(b'<data>')
        for event, elem in ET.iterparse(file_name, events=('start', 'end')):
            if event == 'end' and elem.tag == 'document':
                cat = elem.find('.//cat')
                if cat is not None and cat.text in categorias_deseadas:
                    output.write(ET.tostring(elem, encoding='utf-8'))
                elem.clear()
                i += 1
                if i % 100000 == 0:
                    porcentaje = ((i / total_docs_estimado) * 100)*2.5
                    print(f"Procesados {i} documentos, aproximadamente {porcentaje:.2f}% del total")
        output.write(b'</data>')

filtrar_categorias(RUTA_MOHAMED, CATEGORIAS_DESEADAS, RUTA_DESTINO)
