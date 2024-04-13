import xml.etree.ElementTree as ET

class XBRL_Parser:
    def __init__(self, ficheros_XML):
        self.ficheros_XML = ficheros_XML
        self.ns = {'xbrl': 'http://www.xbrl.org/2003/instance'}
        self.ns1 = {'iic-com': 'http://www.cnmv.es/iic/com/1-2009/2009-03-31'}
        self.dgi = {'dgi-est-gen': 'http://www.xbrl.org.es/es/2008/dgi/gp/est-gen/2008-01-30'}
        
    def parse_fondos(self):
        fondos_data = []
        for fichero_XML in self.ficheros_XML:
            tree = ET.parse(fichero_XML)
            root = tree.getroot()

            identificador = root.find('.//xbrl:identifier', self.ns)
            id = identificador.text
            registro = root.find('.//iic-com:RegistroCNMV', self.ns1)
            reg = int(registro.text)
            direccion = root.find('.//dgi-est-gen:AddressLine', self.dgi)
            dir = direccion.text
            correo = root.find('.//dgi-est-gen:CommunicationValue', self.dgi)
            email = correo.text

            fondos_data.append({'identifier': id, 'registro': reg, 'direccion': dir, 'correo': email})

        return fondos_data
    
    def parse_carteras(self):
        carteras_data = []
        for fichero_XML in self.ficheros_XML:
            tree = ET.parse(fichero_XML)
            root = tree.getroot()
            periodo = fichero_XML.split("_")[1] + "_" + fichero_XML.split("_")[2].split(".")[0]

            elementos = root.findall('.//iic-com:InversionesFinancierasRVCotizada', self.ns1)
            for elemento in elementos:
                nombreF = elemento.find('.//iic-com:InversionesFinancierasDescripcion', self.ns1)
                registro = root.find('.//iic-com:RegistroCNMV', self.ns1)
                importes = elemento.findall('.//iic-com:InversionesFinancierasImporte', self.ns1)

                cartera = {
                    'descripcion': nombreF.text if nombreF is not None else '',
                    'registro': int(registro.text) if registro is not None else 0,
                    'periodo': periodo,
                    'importeValorAct': '',
                    'importeValorAnt': '',
                    'inversionPorcActual': '',
                    'inversionPorcAnterior': ''
                }
 
                for importe in importes:
                    actualOAnt =importe.attrib.get('contextRef')
                    for e in importe:
                        decimals = e.attrib.get('decimals')
                        actualOAnt = e.attrib.get('contextRef').split("_")[3]

                        if decimals == "0": 
                            if actualOAnt == "ia":
                                cartera['importeValorAct'] = e.text
                            else:
                                cartera['importeValorAnt'] = e.text
                        else:
                            if actualOAnt == "ia":
                                cartera['inversionPorcActual'] = e.text
                            else:
                                cartera['inversionPorcAnterior'] = e.text
                carteras_data.append(cartera)
                
        return carteras_data

def obtener_datos():
    ficheros_XML = ['Semestre_1_2022.XML', 'Semestre_2_2022.XML', 'Semestre_1_2023.XML', 'Semestre_2_2023.XML',
                    'Semestre_1_2022_EUR.XML', 'Semestre_2_2022_EUR.XML', 'Semestre_1_2023_EUR.XML', 'Semestre_2_2023_EUR.XML',
                    'Semestre_1_2022_ABANCA.XML', 'Semestre_2_2022_ABANCA.XML', 'Semestre_1_2023_ABANCA.XML', 'Semestre_2_2023_ABANCA.XML',
                    'Semestre_1_2022_AURUM.XML', 'Semestre_2_2022_AURUM.XML', 'Semestre_1_2023_AURUM.XML', 'Semestre_2_2023_AURUM.XML']
    xbrl_parser = XBRL_Parser(ficheros_XML)
    fondos_data = xbrl_parser.parse_fondos()
    carteras_data = xbrl_parser.parse_carteras()
    return fondos_data, carteras_data