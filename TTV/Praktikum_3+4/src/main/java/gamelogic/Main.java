package gamelogic;

import de.uniba.wiai.lspi.chord.data.URL;
import de.uniba.wiai.lspi.chord.service.PropertiesLoader;
import de.uniba.wiai.lspi.chord.service.ServiceException;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import de.uniba.wiai.lspi.util.logging.Logger;

import java.math.BigInteger;
import java.net.MalformedURLException;

public class Main {

	public static int NR_BITS_ID = 160;
	public static BigInteger MAX_ID = BigInteger.valueOf(2).pow(NR_BITS_ID).subtract(BigInteger.ONE);
	private static String propertyFile = "game.properties";
	private static Logger logger = Logger.getLogger(Main.class);

	//TODO: still something missing
	public static void main(String[] args) {
		try {
			if (args.length > 0) {
				propertyFile = args[0];
			}
			logger.info("Welcome to this party");
			Configuration.init(propertyFile);

			ChordImpl chord = initChord();

			networkStuff(chord);
		} catch (Exception e) {
			logger.error("Shutdown game because of error.");
			e.printStackTrace();
		}
	}

	private static ChordImpl initChord() {
		PropertiesLoader.loadPropertyFile();
		ChordImpl chord = new ChordImpl();
		ChordAdapter adapter = new ChordAdapter(chord);
		chord.setCallback(adapter);
		return chord;
	}

	private static ChordImpl networkStuff(ChordImpl chord) throws MalformedURLException, ServiceException {
		String localUrlStr = Configuration.getProperty("localURL");
		String protocol = URL.KNOWN_PROTOCOLS.get(URL.SOCKET_PROTOCOL);
		URL localURL = new URL(protocol + "://" + localUrlStr + "/");
		logger.info("Local URL: " + localUrlStr);

		String bootstrapUrlStr = Configuration.getProperty("joinURL");
		if (bootstrapUrlStr.length() > 0) {
			URL bootstrapUrl = new URL(protocol + "://" + bootstrapUrlStr + "/");
			logger.info("Joining network on node " + bootstrapUrl);
			chord.join(localURL, bootstrapUrl);
		} else {
			logger.info("Create network on node " + localURL);
			chord.create(localURL);
		}

		return chord;
	}
}
