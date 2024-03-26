#!/bin/bash

# Ruta al archivo Saxon JAR
saxon_jar="SaxonJAR11/saxon-he-11.6.jar"

# Nombre del archivo XML
archivo_xml="datos.xml"

# Consulta XQuery
consulta_xquery='
let $qintlValues := //qintl
let $uniqueQintlValues := distinct-values($qintlValues)
for $qintlValue in $uniqueQintlValues
let $count := count($qintlValues[. = $qintlValue])
order by $count descending
return concat("Valor de qintl: ", $qintlValue, ", Número de repeticiones: ", $count)
'

# Ejecutar la consulta XQuery con Saxon
java -jar "$saxon_jar" -?:"$consulta_xquery" -s:"$archivo_xml"

