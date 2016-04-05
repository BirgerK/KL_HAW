package aufgabe;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.vocabulary.DCTerms;
import org.apache.jena.vocabulary.DCTypes;

public class CandleInTheWind {

    public static void main(String[] args) {
        String title = "Candle in the wind";
        String subject = "Diana, Princess of Wales";
        String date = "1997";
        String creator = "John, Elton";
        String type = "sound";
        String description = "Tribute to a dead princess";
        String relation = "IsVersionOf Elton John's 1976 song Candle in the Wind";

        Model model = ModelFactory.createDefaultModel();

        Resource book = model.createResource(DCTypes.Sound);
        book.addProperty(DCTerms.title,title);
        book.addProperty(DCTerms.subject,subject);
        book.addProperty(DCTerms.date,date);
        book.addProperty(DCTerms.creator,creator);
        book.addProperty(DCTerms.type,type);
        book.addProperty(DCTerms.description,description);
        book.addProperty(DCTerms.relation,relation);

        // now write the model in XML form to a file
        System.out.println("Default to file");
        model.write(System.out);
        System.out.println();
    }
}
