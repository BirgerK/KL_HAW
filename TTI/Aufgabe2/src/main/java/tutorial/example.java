package tutorial;

import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.RDFS;

public class example {

    public static void main(String[] args) {
        //vocabulary namespace
        String termsNS = "http://example.com/terms#";
        //instance namespace
        String instanceNS = "http://example.com/instances#";
        Model model = ModelFactory.createDefaultModel();
        //create properties and put them into a hierarchy
        Property subProp = model.createProperty(termsNS, "subProp");
        Property superProp = model.createProperty(termsNS, "superProp");
        model.add(subProp, RDFS.subPropertyOf, superProp);
        //create classes and put them into a hierarchy
        Resource classA = model.createResource(termsNS + "A");
        Resource classB = model.createResource(termsNS + "B");
        classB.addProperty(RDFS.subClassOf, classA);
        //create a resource of type A with property subProp
        Resource a = model.createResource(instanceNS + "a", classB)
                .addProperty(subProp, "foo");
        //create an RDFS model which contains explicit statements as well as those that can be inferred
        InfModel inf = ModelFactory.createRDFSModel(model);
        //retrieve resource "http://example.com/instances#a from the RDFS model
        Resource x = inf.getResource(instanceNS + "a");
        //show all of the resource's properties
        StmtIterator iter = x.listProperties();
        while (iter.hasNext()) {
            Statement stmt = iter.nextStatement(); // get next statement
            Resource subject = stmt.getSubject(); // get the subject
            Property predicate = stmt.getPredicate(); // get the predicate
            RDFNode object = stmt.getObject(); // get the object
            System.out.print(subject.toString());
            System.out.print(" " + predicate.toString() + " ");
            if (object instanceof Resource) {
                System.out.print(object.toString());
            } else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }
            System.out.println(" .");
        }
    }
}
