package tutorial;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.vocabulary.VCARD;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;

public class main4 {

    public static void main(String[] args) throws FileNotFoundException {
        ClassLoader classLoader = new main4().getClass().getClassLoader();
        File file = new File(classLoader.getResource("input.rdf").getFile());
        InputStream inputStream = new FileInputStream(file);

        // create an empty Model
        Model model = ModelFactory.createDefaultModel();
        model.read(inputStream, null);


        // now write the model in XML form to a file
        System.out.println("Default to file");
        model.write(System.out);
        System.out.println();

        // now write the model in XML form to a file
        System.out.println("Modified to file");
        model.write(System.out, "RDF/XML-ABBREV");
        System.out.println();

        // now write the model in N-TRIPLES form to a file
        System.out.println("Triples to file");
        model.write(System.out, "N-TRIPLES");
    }
}
