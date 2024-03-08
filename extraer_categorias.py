import xml.etree.ElementTree as ET

tree = ET.parse('FullOct2007.xml')
root = tree.getroot()

new_root = ET.Element('data')


for document in root.findall('.//document'):
    cat = document.find('.//cat')
    if cat is not None and (cat.text == 'Real Madrid' or cat.text == 'Formula One' or cat.text == 'Music' or cat.text == 'Champions League'):
        print("entra")
        new_root.append(document)

new_tree = ET.ElementTree(new_root)
new_tree.write('categorias.xml', encoding='utf-8')