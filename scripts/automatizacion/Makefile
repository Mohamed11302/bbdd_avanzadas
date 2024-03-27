CARPETA_ORIGEN=../../files
CARPETA_DESTINO=automatizacion_files
CARPETA_SCRIPTS=scripts
CARPETA_CONSULTAS=../../consultas
NOMBRE_ARCHIVO=categorias_filtradas
ARCHIVO_ORIGEN = ${CARPETA_ORIGEN}/${NOMBRE_ARCHIVO}
ARCHIVO_GENERADO = ${CARPETA_DESTINO}/${NOMBRE_ARCHIVO}
SAXONJAR=SaxonJAR/saxon-he-12.4.jar

.PHONY: proceso_xml_automatico

clean: uninstall-dependencies delete-xml-files
all-run: install-dependencies run-xml

install-dependencies:
#	Descargar las herramientas necesarias para ejecutar este proceso 
	sudo apt update
#	TRANG
	sudo apt-get install -y trang
#	SAXON
	sudo apt-get install -y unzip
	wget https://github.com/Saxonica/Saxon-HE/releases/download/SaxonHE12-4/SaxonHE12-4J.zip
#	wget https://github.com/Saxonica/Saxon-HE/releases/download/SaxonHE11-6/SaxonHE11-6J.zip

	unzip SaxonHE12-4J.zip -d SaxonJAR
uninstall-dependencies:
	- rm -rf SaxonHE12-4J.zip SaxonJAR
	sudo apt remove -y libxml2-utils
	sudo apt remove -y trang
	sudo apt remove -y unzip

run-xml:
	@echo "*******************"
	@echo "CREACION CARPETA TRABAJO"
	-mkdir ${CARPETA_DESTINO}
	@echo "************************"
#	Copiar el archivo de entrada para poder trabajar con el sin modificar el original
	@echo "*******************"
	@echo "COPIA ARCHIVOS NECESARIOS"
	cp ${ARCHIVO_ORIGEN}.xml ${ARCHIVO_GENERADO}.xml
	cp ${ARCHIVO_ORIGEN}.xslt ${ARCHIVO_GENERADO}.xslt
	@echo "************************"
#	Crear el archivo dtd
	@echo "*******************"
	@touch ${ARCHIVO_GENERADO}.dtd
	@echo "CREACION DTD"
	trang -I xml -O dtd ${ARCHIVO_GENERADO}.xml ${ARCHIVO_GENERADO}.dtd
	@echo "************************"
#	Añadir la referencia del dtd al xml
	@echo "*******************"
	@echo "AÑADIR REFERENCIA DTD"
	javac ${CARPETA_SCRIPTS}/add_reference_dtd.java
	java -cp ${CARPETA_SCRIPTS} add_reference_dtd ${ARCHIVO_GENERADO}.xml ${NOMBRE_ARCHIVO}.dtd
	@echo "************************"
#	Crear el archivo xsd
	@echo "*******************"
	@echo "CREACION XSD"
	trang ${ARCHIVO_GENERADO}.xml ${ARCHIVO_GENERADO}.xsd
	@echo "************************"
#	Crear el archivo HTML con el formateo correcto
	@echo "*******************"
	@echo "CREACION ARCHIVO HTML"
	java -jar ${SAXONJAR} -s:${ARCHIVO_GENERADO}.xml -xsl:${ARCHIVO_ORIGEN}.xslt -o:${ARCHIVO_GENERADO}XSLT.html
	@echo "************************"
#	Consultas
	@echo "*******************"
	@echo "CONSULTAS"
	javac -cp ${SAXONJAR} -Xdiags:verbose  ${CARPETA_SCRIPTS}/XQueryExecutor.java
	@echo "######## CONSULTA 1 ########"
	java -cp ${CARPETA_SCRIPTS}:${SAXONJAR} XQueryExecutor ${CARPETA_CONSULTAS}/consulta_1.txt ${ARCHIVO_GENERADO}.xml
	@echo "######## CONSULTA 2 ########"
	java -cp ${CARPETA_SCRIPTS}:${SAXONJAR} XQueryExecutor ${CARPETA_CONSULTAS}/consulta_2.txt  ${ARCHIVO_GENERADO}.xml
	@echo "######## CONSULTA 3 ########"
	java -cp ${CARPETA_SCRIPTS}:${SAXONJAR} XQueryExecutor ${CARPETA_CONSULTAS}/consulta_3.txt  ${ARCHIVO_GENERADO}.xml
	@echo "************************"

delete-xml-files:
	- rm -rf ${CARPETA_DESTINO}