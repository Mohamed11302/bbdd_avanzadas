import net.sf.saxon.s9api.*;

import java.io.File;
import java.io.IOException; // Importa IOException

public class XQueryExecutor {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Uso: java XQueryExecutor <ruta_consulta_XQuery> <ruta_archivo_XML>");
            System.exit(1);
        }

        String rutaConsultaXQuery = args[0];
        String rutaArchivoXML = args[1];

        try {
            Processor proc = new Processor(false);
            XQueryCompiler comp = proc.newXQueryCompiler();

            // Manejar IOException al crear un objeto File
            File consultaFile = new File(rutaConsultaXQuery);
            XQueryExecutable exp = comp.compile(consultaFile);
            XQueryEvaluator eval = exp.load();
            DocumentBuilder builder = proc.newDocumentBuilder();
            XdmNode doc = builder.build(new File(rutaArchivoXML));
            eval.setSource(doc.asSource());
            XdmValue value = eval.evaluate();

            for (XdmItem item : value) {
                System.out.println(item.getStringValue());
            }
        } catch (SaxonApiException | IOException e) { // Manejar IOException
            e.printStackTrace();
        }
    }
}
