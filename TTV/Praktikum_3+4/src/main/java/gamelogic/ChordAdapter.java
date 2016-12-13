package gamelogic;

import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.service.NotifyCallback;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import de.uniba.wiai.lspi.util.logging.Logger;
import gamelogic.player.Player;
import gamelogic.player.Players;

public class ChordAdapter implements NotifyCallback {

	private static Logger logger = Logger.getLogger(ChordAdapter.class);
	private ChordImpl chord;
	private boolean gameIsDone = false;

	public ChordAdapter(ChordImpl chord) {
		this.chord = chord;
	}

	public void retrieved(ID target) {
		synchronized (this) {
			logger.info("Retrieved shot at " + target);

			Players.init(chord);

			Players.updatePlayers(chord);
			boolean hit = Shot.isBoom(target);

			Player meT = Players.me;
			meT.addShotShipOnField(target, hit);
			Players.savePlayer(meT);

			logger.info("Been shot at ID: " + target + "; And was a hit: " + hit);
			chord.broadcastAsync(target, hit);

			logger.info("And now let's give them something from the good stuff");
			shoot(chord);
		}
	}

	public void broadcast(ID source, ID target, Boolean hit) {
		synchronized (this) {
			Players.init(chord);

			Player shooter = Players.getPlayer(source);
			if (shooter == null) {
				shooter = Players.createPlayer(source);
				Players.savePlayer(shooter);
				logger.info("New player saved: " + source);
			}

			shooter.addShotShipOnField(target, hit);
			Players.savePlayer(shooter);
			Players.updatePlayers(chord);

			if (shooter.isDefeated()) {
				logger.info("Player with ID " + shooter.getId() + " is defeated.");
				gameIsDone = true;
				if (Players.me.getLastShot() != null && Players.me.getLastShot().equals(target)) {
					logger.warn("_____________!FIRST BLOOD!_____________");
					logger.info("You did the last shot! Well done, my friend.");
				}
			}
		}
	}

	private void shoot(ChordImpl chord) {
		ID shootOnId = Shot.selectIdToShootAt(Shot.selectPlayerToShootAt());
		Player meT = Players.me;
		meT.setLastShot(shootOnId);
		Players.savePlayer(meT);

		chord.retrieveAsync(shootOnId);
	}
}
