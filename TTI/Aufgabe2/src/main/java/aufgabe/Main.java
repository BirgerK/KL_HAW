package aufgabe;

import org.apache.jena.rdf.model.*;
import org.apache.jena.util.iterator.ExtendedIterator;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.RDFS;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {

    //vocabulary namespace
    public static final String termsNS = "http://example.com/terms#";
    //instance namespace
    public static final String instanceNS = "http://example.com/instances#";

    public static void main(String[] args) throws IOException {
        Model model = ModelFactory.createDefaultModel();

        /**
         * DEFINE CLASSES
         */
        Resource song = model.createResource(termsNS + "Song");
        Resource interpretClass = model.createResource(termsNS + "Interpret");
        Resource musicant = model.createResource(termsNS + "Musicant");
        Resource band = model.createResource(termsNS + "Band");
        Resource albumClass = model.createResource(termsNS + "Album");
        Resource genreClass = model.createResource(termsNS + "Genre");


        /**
         * DEFINE CLASS-RELATIONSHIPS
         */
        musicant.addProperty(RDFS.subClassOf, interpretClass);
        band.addProperty(RDFS.subClassOf, interpretClass);


        /**
         * DEFINE PROPERTIES
         */
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
        Property superGenreProperty = model.createProperty(termsNS, "superGenre");


        /**
         * CREATE GENRE
         */
        Resource rock = model.createResource(instanceNS + "rock", genreClass);
        rock.addProperty(name, "Rock");
        Resource kuschelRock = model.createResource(instanceNS + "kuschelrock", genreClass);
        kuschelRock.addProperty(name, "KuschelRock");
        kuschelRock.addProperty(superGenreProperty, rock);
        Resource glamRock = model.createResource(instanceNS + "glamRock", genreClass);
        glamRock.addProperty(name, "GlamRock");
        glamRock.addProperty(superGenreProperty, rock);
        Resource metal = model.createResource(instanceNS + "metal", genreClass);
        rock.addProperty(name, "metal");


        /**
         * CREATE INTERPRETS
         */
        // Slipknot
        Resource coreyTaylor = model.createResource(instanceNS + "CoreyTaylor", interpretClass);
        coreyTaylor.addProperty(name, "Corey Taylor");
        coreyTaylor.addProperty(birthDate, "8.12.1973");
        coreyTaylor.addProperty(nationality, "USA");
        coreyTaylor.addProperty(gender, "male");
        coreyTaylor.addProperty(birthCity, "Des Moines");
        Resource chrisFehn = model.createResource(instanceNS + "ChrisFehn", interpretClass);
        coreyTaylor.addProperty(name, "Chris Fehn");
        coreyTaylor.addProperty(birthDate, "24.02.1972");
        coreyTaylor.addProperty(nationality, "USA");
        coreyTaylor.addProperty(gender, "male");
        coreyTaylor.addProperty(birthCity, "Des Moines");

        Resource slipknot = model.createResource(instanceNS + "slipknot", band);
        RDFNode[] slipknotMembers = new RDFNode[2];
        slipknotMembers[0] = coreyTaylor;
        slipknotMembers[1] = chrisFehn;
        RDFList slipknotMembersList = model.createList(slipknotMembers);
        slipknot.addProperty(name, "Slipknot");
        slipknot.addProperty(members, slipknotMembersList);
        slipknot.addProperty(foundingDay, "1995");
        slipknot.addProperty(genreProperty, kuschelRock);

        //StoneSour
        Resource jamesRoot = model.createResource(instanceNS + "JamesRoot", interpretClass);
        coreyTaylor.addProperty(name, "James Root");
        coreyTaylor.addProperty(birthDate, "02.10.1971");
        coreyTaylor.addProperty(nationality, "USA");
        coreyTaylor.addProperty(gender, "male");
        coreyTaylor.addProperty(birthCity, "Des Moines");

        Resource stonesour = model.createResource(instanceNS + "stonesour", band);
        RDFNode[] stonesourMembers = new RDFNode[2];
        stonesourMembers[0] = coreyTaylor;
        stonesourMembers[1] = jamesRoot;
        RDFList stonesourMembersList = model.createList(stonesourMembers);
        stonesour.addProperty(name, "Stonesour");
        stonesour.addProperty(members, stonesourMembersList);
        stonesour.addProperty(foundingDay, "1992");
        stonesour.addProperty(genreProperty, glamRock);


        /**
         * CREATE ALBUMS
         */
        Resource slipknotAlbum = model.createResource(instanceNS + "Vol3", albumClass);
        slipknotAlbum.addProperty(name, "Vol. 3( Blah Blah)");
        slipknotAlbum.addProperty(interpretProperty, slipknot);
        slipknotAlbum.addProperty(releaseYear, "25.05.2004");
        slipknot.addProperty(genreProperty, kuschelRock);
        slipknot.addProperty(studio, "The Mansion");
        slipknot.addProperty(label, "Roadrunner Records");

        Resource stonesourAlbum = model.createResource(instanceNS + "StoneSour", albumClass);
        slipknotAlbum.addProperty(name, "StoneSour");
        slipknotAlbum.addProperty(interpretProperty, slipknot);
        slipknotAlbum.addProperty(releaseYear, "2002");
        slipknot.addProperty(genreProperty, glamRock);
        slipknot.addProperty(studio, "Catamount Studio");
        slipknot.addProperty(label, "Roadrunner Records");


        /**
         * CREATE SONGS
         */
        Resource songDuality = model.createResource(instanceNS + "Duality", song);
        songDuality.addProperty(title, "Duality");
        songDuality.addProperty(interpretProperty, slipknot);
        songDuality.addProperty(genreProperty, kuschelRock);
        songDuality.addProperty(albumProperty, slipknotAlbum);
        songDuality.addProperty(releaseYear, "2004");
        songDuality.addProperty(language, "English");

        Resource songBlotter = model.createResource(instanceNS + "Blotter", song);
        songBlotter.addProperty(title, "Blotter");
        songBlotter.addProperty(interpretProperty, stonesour);
        songBlotter.addProperty(genreProperty, glamRock);
        songBlotter.addProperty(albumProperty, stonesourAlbum);
        songBlotter.addProperty(releaseYear, "2002");
        songBlotter.addProperty(language, "English");


        writeModel(model);
        
        
        InfModel infModel = ModelFactory.createRDFSModel(model);
		 
        //########### Statements ###############
        
        //Search Song with language english
		ResIterator iter1 = infModel.listResourcesWithProperty(language, "English");
		while(iter1.hasNext()){
			Statement songStatement1 = iter1.nextResource().getProperty(title);
			RDFNode songName1 = songStatement1.getObject();
			System.out.println(songName1);
		}
        
        //Search Songs released in Year 2004
		ResIterator iter = infModel.listResourcesWithProperty(releaseYear, "2004");
		while(iter.hasNext()){
			Statement songStatement = iter.nextResource().getProperty(title);
			RDFNode songName = songStatement.getObject();
			System.out.println(songName);
		}

        //Mega CoreyTaylor-Search!
        List<Resource> songsWithCoreyTaylor = new ArrayList<Resource>();
        ResIterator bandsWithMembers = infModel.listResourcesWithProperty(members);

        while (bandsWithMembers.hasNext()) {
            Resource tempBandWithMembers = bandsWithMembers.next();
            ExtendedIterator<RDFNode> bandMembers = tempBandWithMembers.getProperty(members).getObject().as(RDFList.class).iterator();

            while (bandMembers.hasNext()) {
                Resource tempBandMember = bandMembers.next().as(Resource.class);
                if (tempBandMember.equals(coreyTaylor)) {
                    ResIterator songsByBand = infModel.listResourcesWithProperty(interpretProperty, tempBandWithMembers);

                    while (songsByBand.hasNext()) {
                        Resource tempInterpretedStuffByBand = songsByBand.next();
                        if (isSong(tempInterpretedStuffByBand)) {
                            songsWithCoreyTaylor.add(tempInterpretedStuffByBand);
                        }
                    }
                }
            }
        }

        System.out.println(songsWithCoreyTaylor);
    }

    public static void writeModel(Model model) {
        System.out.println("created model");
        model.write(System.out);
        System.out.println();
    }

    public static boolean isSong(Resource resource) {
        return resource.getProperty(RDF.type).getObject().toString().equals(termsNS + "Song");
    }
}
