package aufgabe;

import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.DCTerms;

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

        Resource theirLieblingsBuch = searchLieblingsbuch(model);

        // print Lieblingsbuch
        if(theirLieblingsBuch != null) {
            System.out.println("Ihr Lieblingsbuch ist: " + theirLieblingsBuch.getProperty(DCTerms.title));
        } else {
            System.out.println("Sie haben kein Lieblingsbuch angegeben!");
        }

        // now write the model in XML form to a file
        System.out.println("imported file");
        model.write(System.out);
        System.out.println();
    }

    public static Resource searchLieblingsbuch(Model model) {
        Resource result = null;

        // list the statements in the Model
        StmtIterator iter = model.listStatements();

        // print out the predicate, subject and object of each statement
        while (iter.hasNext()) {
            Statement stmt      = iter.nextStatement();  // get next statement
            Resource  subject   = stmt.getSubject();     // get the subject
            Property  predicate = stmt.getPredicate();   // get the predicate
            RDFNode   object    = stmt.getObject();      // get the object

            if(predicate.toString().toLowerCase().equals("subject") && object.toString().toLowerCase().contains("Architecture")) {
                result = subject;
                break;
            }
        }

        return result;
    }
}
