import xml.etree.ElementTree as ET #no funciona pero es mas eficiente (arreglarlo mas adelante)
import os   
RUTA_MOHAMED = 'C:\\Users\\mohae\\Desktop\\2º Semestre\\BBDD Avanzadas\\Bloques\\Bloque 2 Xml\\Trabajo\\Trabajo 1\\FullOct2007.xml'
CATEGORIAS_DESEADAS = set(['Video & Online Games', 'Music & Music Players', 'Reality Television', 'Other - Entertainment'])



def filtrar_categorias(file_name, categorias_deseadas):
    new_data = ET.Element('data')
    total_documents = os.path.getsize(file_name)
    processed_documents = 0
    print_every = 1000000
    for event, elem in ET.iterparse(file_name, events=('start',)):
        #if event == 'start' or event=='end':
        if event=='start':
            if elem.tag == 'document':
                total_documents += 1
                cat = elem.find('cat')
                #print("FOUND DOCUMENT (START)")
                #print(cat.text if cat is not None else None)
                if cat is not None and cat.text in categorias_deseadas:
                    #print(f"EN LAS CATEGORIAS {cat.text}")
                    #print(ET.tostring(elem, encoding='unicode'))
                    new_elem = copy_element(elem)
                    new_data.append(new_elem)
        processed_documents += len(elem.tag) + (len(elem.text) if elem.text else 0) + 2  # Approximate size of the element in the file
        if processed_documents % print_every == 0:  # Update progress 
            print(f"Processed {processed_documents / 1024 / 1024:.2f}MB of {total_documents / 1024 / 1024:.2f}MB ({100.0 * processed_documents / total_documents:.2f}%)")
        elem.clear()
    return new_data


def copy_element(elem):
    new_elem = ET.Element(elem.tag)
    for key, value in elem.attrib.items():
        new_elem.set(key, value)
    for child in elem:
        new_child = copy_element(child)
        new_elem.append(new_child)
    new_elem.text = elem.text
    return new_elem


new_data = filtrar_categorias(RUTA_MOHAMED, CATEGORIAS_DESEADAS)

# Crear un nuevo objeto ElementTree y usar el método write en él
new_tree = ET.ElementTree(new_data)
new_tree.write('categorias4.xml', encoding='utf-8')
