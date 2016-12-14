package gamelogic;

import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.data.URL;
import de.uniba.wiai.lspi.chord.service.PropertiesLoader;
import de.uniba.wiai.lspi.chord.service.ServiceException;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import org.apache.log4j.Logger;

import java.math.BigInteger;
import java.net.MalformedURLException;
import java.util.*;

public class Main {

	public static int NR_BITS_ID = 160;
	public static BigInteger MAX_ID = BigInteger.valueOf(2).pow(NR_BITS_ID).subtract(BigInteger.ONE);
	public static Set<Integer> fieldsWithShips;
	private static String propertyFile = "game.properties";
	private static Logger logger = Logger.getLogger(Main.class);
	private static gamelogic.ChordAdapter adapter;

	public static void main(String[] args) {
		try {
			if (args.length > 0) {
				propertyFile = args[0];
			}
			logger.error("Welcome to this party");
			Configuration.init(propertyFile);
			fieldsWithShips = fillFields(Integer.valueOf(Configuration.getProperty("shipsPerPlayer")),
					Integer.valueOf(Configuration.getProperty("fieldsPerPlayer")));
			ChordImpl chord = initChord();

			chord = networkStuff(chord);

			logger.error("Duell is starting: Your ID is " + chord.getID());

			if (ID.valueOf(MAX_ID).isInInterval(chord.getPredecessorID(), chord.getID()) || MAX_ID
					.equals(chord.getID().toBigInteger())) {
				logger.error("Press the red big button to do the first shot");
				System.in.read();
				adapter.firstShoot();
			}
		} catch (Exception e) {
			logger.error("Shutdown game because of error.");
			e.printStackTrace();
		}
	}

	private static ChordImpl initChord() {
		PropertiesLoader.loadPropertyFile();
		ChordImpl chord = new ChordImpl();
		adapter = new ChordAdapter(chord);
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

	private static Set<Integer> fillFields(int nrShips, int nrFields) {
		logger.info("Fill fields with ships");
		Set<Integer> fieldsWithShips = new HashSet<Integer>();
		List<Integer> fields = new ArrayList<Integer>();
		for (int i = 0; i < nrFields; i++) {
			fields.add(i);
		}
		Random r = new Random();
		for (int i = 0; i < nrShips; i++) {
			int fIndex = r.nextInt(fields.size());
			fieldsWithShips.add(fields.get(fIndex));
			fields.remove(fIndex);
		}
		logger.info("Fields with ships: " + fieldsWithShips);
		return fieldsWithShips;
	}
}
