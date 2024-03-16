import xml.etree.ElementTree as ET

def contar_documentos(file_path):
    # Parsear el archivo XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Contar el número de elementos 'document'
    num_documentos = len(root.findall('document'))

    return num_documentos

# Ruta al archivo XML
archivo_xml = 'categorias5.xml'

# Contar documentos
numero_documentos = contar_documentos(archivo_xml)
print(f'Número de documentos en el archivo XML: {numero_documentos}')
