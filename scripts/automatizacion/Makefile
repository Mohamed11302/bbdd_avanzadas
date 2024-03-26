CARPETA_ORIGEN=../../files
CARPETA_DESTINO=automatizacion_files
CARPETA_SCRIPTS=scripts
NOMBRE_ARCHIVO=categorias_filtradas
ARCHIVO_ORIGEN = ${CARPETA_ORIGEN}/${NOMBRE_ARCHIVO}
ARCHIVO_GENERADO = ${CARPETA_DESTINO}/${NOMBRE_ARCHIVO}

.PHONY: proceso_xml_automatico

clean: uninstall-dependencies delete-xml-files

install-dependencies:
#	Descargar las herramientas necesarias para ejecutar este proceso 
	sudo apt update
#	XMLLINT	
	sudo apt install -y libxml2-utils
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
	@echo "*******************"
#	Copiar el archivo de entrada para poder trabajar con el sin modificar el original
	@echo "*******************"
	@echo "COPIA ARCHIVOS NECESARIOS"
	cp ${ARCHIVO_ORIGEN}.xml ${ARCHIVO_GENERADO}.xml
	cp ${ARCHIVO_ORIGEN}.xslt ${ARCHIVO_GENERADO}.xslt
	@echo "*******************"
#	Crear el archivo dtd
	@echo "*******************"
	@touch ${ARCHIVO_GENERADO}.dtd
	@echo "CREACION DTD"
	trang -I xml -O dtd ${ARCHIVO_GENERADO}.xml ${ARCHIVO_GENERADO}.dtd
	@echo "*******************"
#	Añadir la referencia del dtd al xml
	@echo "*******************"
	@echo "AÑADIR REFERENCIA DTD"
	javac ${CARPETA_SCRIPTS}/add_reference_dtd.java
	java -cp ${CARPETA_SCRIPTS} add_reference_dtd ${ARCHIVO_GENERADO}.xml ${NOMBRE_ARCHIVO}.dtd
	@echo "*******************"
#	Crear el archivo HTML con el formateo correcto
	@echo "*******************"
	@echo "CREACION ARCHIVO HTML"
	java -jar SaxonJAR/saxon-he-12.4.jar -s:${ARCHIVO_GENERADO}.xml -xsl:${ARCHIVO_ORIGEN}.xslt -o:${ARCHIVO_GENERADO}XSLT.html
	@echo "*******************"
#	Consultas
	@echo "*******************"
	@echo "CONSULTAS"
	javac -cp SaxonJAR/saxon-he-12.4.jar -Xdiags:verbose  scripts/XQueryExecutor.java
	@echo "######## CONSULTA 1 ########"
	java -cp scripts:SaxonJAR/saxon-he-12.4.jar XQueryExecutor "../../consultas/consulta_1.txt" "automatizacion_files/categorias_filtradas.xml"
	@echo "######## CONSULTA 2 ########"
	java -cp scripts:SaxonJAR/saxon-he-12.4.jar XQueryExecutor "../../consultas/consulta_2.txt" "automatizacion_files/categorias_filtradas.xml"
	@echo "######## CONSULTA 3 ########"
	java -cp scripts:SaxonJAR/saxon-he-12.4.jar XQueryExecutor "../../consultas/consulta_3.txt" "automatizacion_files/categorias_filtradas.xml"
	@echo "*******************"

delete-xml-files:
	- rm -rf automatizacion_files