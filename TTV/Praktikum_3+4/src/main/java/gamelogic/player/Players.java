package gamelogic.player;

import de.uniba.wiai.lspi.chord.com.Node;
import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import de.uniba.wiai.lspi.util.logging.Logger;
import gamelogic.Configuration;

import java.math.BigInteger;
import java.util.*;

public class Players {

	public static Player me = null;
	private static Logger logger = Logger.getLogger(Players.class);
	private static Map<ID, Player> players = null;

	public static void init(ChordImpl chord) {
		if (players == null) {
			players = new HashMap();
			ID ownId = chord.getID();
			ID predId = chord.getPredecessorID();
			int shipsPerPlayer = Integer.valueOf(Configuration.getProperty("shipsPerPlayer"));
			int fieldsPerPlayer = Integer.valueOf(Configuration.getProperty("fieldsPerPlayer"));

			logger.info("Initialisation of player map: Your Range: From " + predId.toBigInteger().add(BigInteger.ONE)
					+ " to " + ownId.toBigInteger());
			Player self = new Player(ownId, shipsPerPlayer, fieldsPerPlayer);
			self.setStartField(ID.valueOf(predId.toBigInteger()
					.add(BigInteger.ONE)));//Start field of ourself is one higher then the ID of our predecessor

			me = self;
			Players.put(ownId, self);
			Players.put(predId, new Player(predId, shipsPerPlayer, fieldsPerPlayer));
		}
	}

	public static void importFingerTable(ChordImpl chord) {
		logger.info("Import FingerTable to Players");

		int shipsPerPlayer = Integer.valueOf(Configuration.getProperty("shipsPerPlayer"));
		int fieldsPerPlayer = Integer.valueOf(Configuration.getProperty("fieldsPerPlayer"));

		for (Node node : chord.getFingerTable()) {
			ID nodeId = node.getNodeID();
			if (players.containsKey(nodeId)) {
				logger.info("Add player with nodeId " + nodeId);
				Player newPlayer = new Player(nodeId, shipsPerPlayer, fieldsPerPlayer);
				players.put(nodeId, newPlayer);
			}
		}
	}

	public static void put(ID id, Player player) {
		players.put(id, player);
	}

	public static List<Player> getAll() {
		List<Player> l = new ArrayList<Player>(players.values());
		Collections.sort(l);
		return l;
	}
}
