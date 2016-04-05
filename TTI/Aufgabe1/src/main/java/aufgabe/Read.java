package aufgabe;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;

import java.io.*;

public class Read {

    public static void main(String[] args) throws FileNotFoundException {
        String input = "./output.rdf";
        if(args.length == 0 && input.length() == 0) {
            System.out.println("It's empty");
            System.exit(1);
        } else if(args.length > 0) {
            input = args[0];
        }

        File file = new File(input);
        InputStream inputStream = new FileInputStream(file);

        Model model = ModelFactory.createDefaultModel();
        model.read(inputStream,null);

        // now write the model in XML form to a file
        System.out.println("Dimported file");
        model.write(System.out);
        System.out.println();
    }
}
