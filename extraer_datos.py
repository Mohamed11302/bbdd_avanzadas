import xml.etree.ElementTree as ET

class XBRL_Parser:
    def __init__(self, ficheros_XML):
        self.ficheros_XML = ficheros_XML
        self.ns = {'xbrl': 'http://www.xbrl.org/2003/instance'}
        self.ns1 = {'iic-com': 'http://www.cnmv.es/iic/com/1-2009/2009-03-31'}
        self.dgi = {'dgi-est-gen': 'http://www.xbrl.org.es/es/2008/dgi/gp/est-gen/2008-01-30'}
        
    def parse(self):
        data = []
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

            data.append({'identifier': id, 'registro': reg, 'direccion': dir, 'correo': email})

        return data

if __name__ == '__main__':
    ficheros_XML = ['Semestre_1_2022.XML', 'Semestre_2_2022.XML', 'Semestre_1_2023.XML', 'Semestre_2_2023.XML']
    xbrl_parser = XBRL_Parser(ficheros_XML)
    data = xbrl_parser.parse()
    print(data)