import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class add_reference_dtd {
    public static void main(String[] args) {
        // Verificar si se proporciona el nombre del archivo XML y DTD como argumentos
        if (args.length != 2) {
            System.out.println("Uso: java AddDoctype nombre_del_archivo.xml nombre_del_archivo.dtd");
            System.exit(1);
        }

        // Obtener los nombres de los archivos XML y DTD de los argumentos de línea de comandos
        String nombreArchivoXML = args[0];
        String nombreArchivoDTD = args[1];

        // Llamar a la función para agregar la línea DOCTYPE si no está presente
        agregarDoctypeSiNoPresente(nombreArchivoXML, nombreArchivoDTD);
    }

    public static void agregarDoctypeSiNoPresente(String nombreArchivoXML, String nombreArchivoDTD) {
        String doctypeLinea = "<!DOCTYPE data SYSTEM \"" + nombreArchivoDTD + "\">";

        try {
            // Leer el archivo original y almacenar su contenido en una lista
            BufferedReader br = new BufferedReader(new FileReader(nombreArchivoXML));
            StringBuilder sb = new StringBuilder();
            String linea;
            boolean doctypePresente = false;
            int lineaNumero = 0;
            while ((linea = br.readLine()) != null) {
                sb.append(linea).append("\n");
                lineaNumero++;
                // Verificar si la línea DOCTYPE ya está presente
                if (lineaNumero == 2 && linea.trim().equals(doctypeLinea.trim())) {
                    doctypePresente = true;
                    break;
                }
            }
            br.close();

            // Si el DOCTYPE no está presente, insertarlo en la segunda línea
            if (!doctypePresente) {
                sb.insert(sb.indexOf("\n") + 1, doctypeLinea + "\n");
                // Escribir el contenido modificado de vuelta al archivo
                BufferedWriter bw = new BufferedWriter(new FileWriter(nombreArchivoXML));
                bw.write(sb.toString());
                bw.close();
            }

        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
