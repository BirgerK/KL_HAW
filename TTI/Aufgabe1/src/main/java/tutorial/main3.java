package tutorial;

import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.VCARD;

public class main3 {

    public static void main(String[] args) {
        // some definitions
        String personURI    = "http://somewhere/JohnSmith";
        String givenName    = "John";
        String familyName   = "Smith";
        String fullName     = givenName + " " + familyName;

        // create an empty Model
        Model model = ModelFactory.createDefaultModel();

        // create the resource
        //   and add the properties cascading style
        Resource johnSmith
                = model.createResource(personURI)
                .addProperty(VCARD.FN, fullName)
                .addProperty(VCARD.N,
                        model.createResource()
                                .addProperty(VCARD.Given, givenName)
                                .addProperty(VCARD.Family, familyName));


        // now write the model in XML form to a file
        System.out.println("Default to file");
        model.write(System.out);

        // now write the model in XML form to a file
        System.out.println("Modified to file");
        model.write(System.out, "RDF/XML-ABBREV");

        // now write the model in N-TRIPLES form to a file
        System.out.println("Triples to file");
        model.write(System.out, "N-TRIPLES");
    }
}
