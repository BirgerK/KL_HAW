package aufgabe;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.vocabulary.RDFS;

import java.io.IOException;

public class Main {

    //vocabulary namespace
    public static final String termsNS = "http://example.com/terms#";
    //instance namespace
    public static final String instanceNS = "http://example.com/instances#";

    public static void main(String[] args) throws IOException {
        Model model = ModelFactory.createDefaultModel();

        // DEFINE CLASSES
        Resource song = model.createResource(termsNS + "Song");
        Resource interpretClass = model.createResource(termsNS + "Interpret");
        Resource musicant = model.createResource(termsNS + "Musicant");
        Resource band = model.createResource(termsNS + "Band");
        Resource albumClass = model.createResource(termsNS + "Album");
        Resource genreClass = model.createResource(termsNS + "Genre");

        // DEFINE CLASS-RELATIONSHIPS
        musicant.addProperty(RDFS.subClassOf, interpretClass);
        band.addProperty(RDFS.subClassOf, interpretClass);
        genreClass.addProperty(RDFS.subClassOf, genreClass);

        // DEFINE PROPERTIES
        Property title = model.createProperty(termsNS, "title");
        Property interpretProperty = model.createProperty(termsNS, "interpret");
        Property genreProperty = model.createProperty(termsNS, "genre");
        Property albumProperty = model.createProperty(termsNS, "album");
        Property releaseYear = model.createProperty(termsNS, "release-year");
        Property mitwirkendeInterpreten = model.createProperty(termsNS, "mitwirkendeInterpreten");
        Property language = model.createProperty(termsNS, "language");
        Property name = model.createProperty(termsNS, "name");
        Property birthDate = model.createProperty(termsNS, "birth-date");
        Property nationality = model.createProperty(termsNS, "nationality");
        Property birthCity = model.createProperty(termsNS, "birthCity");
        Property gender = model.createProperty(termsNS, "gender");
        Property members = model.createProperty(termsNS, "members");
        Property foundingDay = model.createProperty(termsNS, "founding-day");
        Property studio = model.createProperty(termsNS, "studio");
        Property label = model.createProperty(termsNS, "label");


    }
}
