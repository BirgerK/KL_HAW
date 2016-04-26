package aufgabe;

import org.apache.commons.io.FileUtils;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.vocabulary.DCTerms;
import org.apache.jena.vocabulary.DCTypes;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

public class Create {

    public static void main(String[] args) throws IOException {
        ClassLoader classLoader = new Create().getClass().getClassLoader();
        File file = new File(classLoader.getResource("aufgabe/input.json").getFile());

        JSONObject jsonInput = new JSONObject(FileUtils.readFileToString(file, Charset.defaultCharset()));
        JSONArray inputArray = jsonInput.getJSONArray("books");

        Model model = ModelFactory.createDefaultModel();

        for (int i = 0, size = inputArray.length(); i < size; i++) {

            JSONObject bookAsJson = inputArray.getJSONObject(i);
            Resource book = model.createResource(DCTypes.Text);

            if(bookAsJson.has("title")) {
                book.addProperty(DCTerms.title, bookAsJson.getString("title"));
            }
            if(bookAsJson.has("subject")) {
                book.addProperty(DCTerms.subject, bookAsJson.getString("subject"));
            }
            if(bookAsJson.has("author")) {
                book.addProperty(DCTerms.creator, bookAsJson.getString("author"));
            }
        }

        // now write the model in XML form to a file
        System.out.println("Default to file");
        model.write(System.out);
        System.out.println();
    }
}
