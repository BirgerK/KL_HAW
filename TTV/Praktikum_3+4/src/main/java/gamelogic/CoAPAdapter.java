package gamelogic;

import de.uniba.wiai.lspi.util.logging.Logger;
import org.eclipse.californium.core.CoapClient;
import org.eclipse.californium.core.CoapResponse;
import org.eclipse.californium.core.coap.MediaTypeRegistry;

import java.net.URI;
import java.net.URISyntaxException;

import org.eclipse.californium.core.Utils;

/**
 * Created by Mooni on 18.12.2016.
 */
public class CoAPAdapter {

    private static Logger logger = Logger.getLogger(CoAPAdapter.class);
    private URI uri = null;
    private static CoapClient client = null;

    public void initLED() throws URISyntaxException {
        uri = new URI("coap://localhost/led");
        client = new CoapClient(uri);
        CoapResponse response = client.get();
        sendStatus(1);

        if (response!=null) {

            System.out.println(response.getCode());
            System.out.println(response.getOptions());
            System.out.println(response.getResponseText());

            System.out.println("\nADVANCED\n");
            // access advanced API with access to more details through .advanced()
            System.out.println(Utils.prettyPrint(response));

        } else {
            System.out.println("No response received.");
        }
    }



    public void sendStatus(int status){
        String color = "g";
        //TODO Hier die das Senden an die LED implementieren
        if(status > 0.5){
            //Grün
            client.put("0", MediaTypeRegistry.TEXT_PLAIN);
            client.put("g", MediaTypeRegistry.TEXT_PLAIN);
        }else if(status <= 0.5 && status > 0){
            //sende Violett
            client.put("1", MediaTypeRegistry.TEXT_PLAIN);
            client.put("g", MediaTypeRegistry.TEXT_PLAIN);
        }else if(status == 0){
            //sende rot
            client.put("0", MediaTypeRegistry.TEXT_PLAIN);
            client.put("r", MediaTypeRegistry.TEXT_PLAIN);
        }else{
            logger.warn("unbekannter Status übergeben in CoAP Adapter");
        }
    }

    public String getStatus(){
        String result = null;

        return result;
    }
}
