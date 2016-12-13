package gamelogic.player;

import de.uniba.wiai.lspi.chord.com.Node;
import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import de.uniba.wiai.lspi.util.logging.Logger;
import gamelogic.Configuration;
import gamelogic.Main;

import java.math.BigInteger;
import java.util.*;

public class Players {

	public static Player me = null;
	private static Logger logger = Logger.getLogger(Players.class);
	private static Map<ID, Player> players = null;

	private static int shipsPerPlayer;
	private static int fieldsPerPlayer;

	public static void init(ChordImpl chord) {
		if (players == null) {
			players = new HashMap<ID, Player>();
			ID ownId = chord.getID();
			ID predId = chord.getPredecessorID();
			shipsPerPlayer = Integer.valueOf(Configuration.getProperty("shipsPerPlayer"));
			fieldsPerPlayer = Integer.valueOf(Configuration.getProperty("fieldsPerPlayer"));

			logger.info("Initialisation of player map: Your Range: From " + predId.toBigInteger().add(BigInteger.ONE)
					+ " to " + ownId.toBigInteger());
			Player self = createPlayer(ownId);
			self.setStartField(ID.valueOf(predId.toBigInteger()
					.add(BigInteger.ONE))); //Start field of ourself is one higher then the ID of our predecessor

			me = self;
			savePlayer(self);
			savePlayer(new Player(predId, shipsPerPlayer, fieldsPerPlayer));
		}
	}

	public static void updatePlayers(ChordImpl chord) {
		importFingerTable(chord);
		updateEstimatedStartingField();
	}

	private static void importFingerTable(ChordImpl chord) {
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

	private static void updateEstimatedStartingField() {
		List<Player> player_list = new ArrayList<Player>(getAll());
		Collections.sort(player_list);

		ID lastId = player_list.get(player_list.size() - 1).getId();
		for (Player p : player_list) {
			BigInteger newId = lastId.toBigInteger().add(BigInteger.ONE);
			if (newId.compareTo(Main.MAX_ID) > 0) {
				newId = newId.subtract(Main.MAX_ID);
			}
			p.setStartField(ID.valueOf(newId));
			savePlayer(p);
			lastId = p.getId();
			logger.info("New range of player " + p.getId() + ": From " + newId + " to " + lastId.toBigInteger());
		}
	}

	public static Player getPlayer(ID id) {
		if (players != null) {
			return players.get(id);
		} else {
			return null;
		}
	}

	public static Player createPlayer(ID playerId) {
		return new Player(playerId, shipsPerPlayer, fieldsPerPlayer);
	}

	public static void savePlayer(Player newPlayer) {
		Players.put(newPlayer.getId(), newPlayer);
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
