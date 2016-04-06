package aufgabe;

import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.DCTerms;

import java.io.*;

import static org.apache.jena.enhanced.BuiltinPersonalities.model;

public class Read {

    public static void main(String[] args) throws FileNotFoundException {
        String input = "./books.rdf";
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
            System.out.println("Ihr Lieblingsbuch ist: " + theirLieblingsBuch.getProperty(DCTerms.title).getObject());
            System.out.println("Das komplette Buch ist: " + resourceAsString(theirLieblingsBuch));
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

            if(predicate.toString().equals(DCTerms.subject.toString()) && object.toString().toLowerCase().contains("architecture")) {
                result = subject;
                break;
            }
        }

        return result;
    }

    public static String resourceAsString(Resource resource) {
        String result = "";

        StmtIterator iter = resource.listProperties();

        while (iter.hasNext()) {
            Statement stmt      = iter.nextStatement();  // get next statement
            Resource  subject   = stmt.getSubject();     // get the subject
            Property  predicate = stmt.getPredicate();   // get the predicate
            RDFNode   object    = stmt.getObject();      // get the object

            result += subject.toString();
            result += " " + predicate.toString() + " ";
            if (object instanceof Resource) {
                result += object.toString();
            } else {
                // object is a literal
                result += " \"" + object.toString() + "\"";
            }

            result += " .";
        }

        return result;
    }
}
