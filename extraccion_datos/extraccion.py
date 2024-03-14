import xml.etree.ElementTree as ET

RUTA_MOHAMED = 'C:\\Users\\mohae\\Desktop\\2º Semestre\\BBDD Avanzadas\\Bloques\\Bloque 2 Xml\\Trabajo\\Trabajo 1\\FullOct2007.xml'
CATEGORIAS_DESEADAS = ['Video & Online Games', 'Music & Music Players', 'Reality Television', 'Other - Entertainment']

def filtrar_categorias(file_name, categorias_deseadas):
    print("Cargando archivo...")
    root = ET.parse(file_name)
    root = root.getroot()
    new_data = ET.Element('data')
    i = 0
    print("Comenzando a filtrar")
    for document in root.findall(".//document"):
        cat = document.find('.//cat')
        if cat is not None and (cat.text in categorias_deseadas):
            new_data.append(document)
        i+=1
        if i % 1000000 == 0:
            print(i)
    return new_data

new_data = filtrar_categorias(RUTA_MOHAMED, CATEGORIAS_DESEADAS)

# Crear un nuevo objeto ElementTree y usar el método write en él
new_tree = ET.ElementTree(new_data)
new_tree.write('categorias2.xml', encoding='utf-8')