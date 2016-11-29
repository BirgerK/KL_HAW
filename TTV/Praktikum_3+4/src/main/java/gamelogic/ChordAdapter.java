package gamelogic;

import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.service.NotifyCallback;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import de.uniba.wiai.lspi.util.logging.Logger;
import gamelogic.player.Players;

public class ChordAdapter implements NotifyCallback {

	private static Logger logger = Logger.getLogger(ChordAdapter.class);
	private ChordImpl chord;

	public ChordAdapter(ChordImpl chord) {
		this.chord = chord;
	}

	public void retrieved(ID target) {
		synchronized (this) {
			logger.info("Retrieved shot at " + target);

			Players.init(chord);

			Players.importFingerTable(chord);
			boolean hit = Shot.isBoom(target);
			Players.me.addShotShipOnField(target, hit);
			logger.info("Shot at Hash: " + target + "; And was a hit: " + hit);
			chord.broadcastAsync(target, hit);
			logger.info("I'm a pacifist. Just make more love. I won't bother this game anymore. idiot.");
		}
	}

	public void broadcast(ID source, ID target, Boolean hit) {

	}
}
