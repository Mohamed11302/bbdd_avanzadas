#!/bin/bash

# Nombre del archivo XML
xml_file="files/categorias_filtradas.xml"

# Obtener valores únicos de <cat>
unique_cats=$(xmllint --xpath '//cat/text()' "$xml_file" | sed 's/&amp;/\&/g' | sort | uniq)

# Iterar sobre los valores únicos y contar su frecuencia
echo "Número de documentos para cada valor de <cat>:"
while IFS= read -r cat_line; do
    # Eliminar espacios en blanco al principio y al final de la línea
    cat_line=$(echo "$cat_line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    # Contar cuántas veces aparece la categoría
    count=$(xmllint --xpath "count(//cat[text()='$cat_line'])" "$xml_file")
    echo "$cat_line: $count"
done <<< "$unique_cats"