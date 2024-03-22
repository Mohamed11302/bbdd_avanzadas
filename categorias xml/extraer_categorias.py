import xml.etree.ElementTree as ET
from collections import Counter
import os

RUTA_MOHAMED = 'C:\\Users\\mohae\\Desktop\\2º Semestre\\BBDD Avanzadas\\Bloques\\Bloque 2 Xml\\Trabajo\\Trabajo 1\\FullOct2007.xml'


def count_elements(file_name, element_names):
    counters = {name: Counter() for name in element_names}
    total_size = os.path.getsize(file_name)
    processed_size = 0
    for event, elem in ET.iterparse(file_name, events=("start", "end")):
        if (event == "start" or event=="end") and elem.tag in element_names:
            counters[elem.tag][elem.text] += 1
        processed_size += len(elem.tag) + (len(elem.text) if elem.text else 0) + 2  # Approximate size of the element in the file
        if processed_size % 1000000 == 0:  # Update progress every 1MB
            print(f"Processed {processed_size / 1024 / 1024:.2f}MB of {total_size / 1024 / 1024:.2f}MB ({100.0 * processed_size / total_size:.2f}%)")
        elem.clear()  # Free up memory
    return counters

def write_counter_to_file(counter, element_name):
    with open(f"{element_name}_counts.txt", "w") as f:
        for key, value in counter.most_common():
            f.write(f"{key}: {value}\n")


for element_name in ["maincat", "cat", "subcat"]:
    counters = count_elements(RUTA_MOHAMED, ["maincat", "cat", "subcat"])
    write_counter_to_file(counters[element_name], element_name)
