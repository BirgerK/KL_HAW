package gamelogic;

import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.service.NotifyCallback;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;
import de.uniba.wiai.lspi.util.logging.Logger;
import gamelogic.player.Field;
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
			logger.error("Retrieved shot at " + target);

			Players.init(chord);

			Players.updatePlayers(chord);
			Field hitField = Shot.isBoom(target);

			Player meT = Players.me;
			meT.shotAtField(target, (hitField != null));
			Players.savePlayer(meT);

			if (hitField != null) {
				Players.me.removeShipFromField(hitField.getFieldNumber());
				//calc status of player and send it to CoapAdapter
				int hits = meT.getHitCounter();
				int shipsTotal = meT.getNumber_of_ships();
				int status = (hits*100)/shipsTotal;
				CoAPAdapter coap = new CoAPAdapter();
				coap.sendStatus(status);

				logger.error("Been shot at ID: " + target + "; And was a hit: " + hitField);
				logger.error("My status: " + Players.me);
			} else {
				logger.info("Been shot at ID: " + target + "; And was a hit: " + hitField);
			}
			chord.broadcastAsync(target, (hitField != null));

			logger.info("And now let's give them something from the good stuff");
			shoot(chord);
		}
	}

	public void broadcast(ID source, ID target, Boolean hit, int transactionNumber) {
		synchronized (this) {
			Players.init(chord);

			Player shooter = Players.getPlayer(source);
			if (shooter == null) {
				shooter = Players.createPlayer(source);
				Players.savePlayer(shooter);
				logger.info("New player saved: " + source);
			}

			if (hit) {
				logger.error("There was a shot at player: " + source + "; And was a hit: " + hit);
			} else {
				logger.info("There was a shot at player: " + source + "; And was a hit: " + hit);
			}

			shooter.shotAtField(target, hit);
			Players.savePlayer(shooter);
			Players.updatePlayers(chord);

			if (shooter.isDefeated()) {
				logger.error(
						"Player with ID " + shooter.getId() + " is defeated in transaction " + transactionNumber + ".");
				gameIsDone = true;
				if (Players.me.getLastShot() != null && Players.me.getLastShot().equals(target)) {
					logger.error("_____________!FIRST BLOOD!_____________");
					logger.error(
							"You did the last shot! Well done, my friend. Won in transaction " + transactionNumber);
				}
				if (shooter.getId().equals(Players.me.getId())) {
					logger.error("_____________!YOU LOST!_____________");
				}
			}
		}
	}

	public void firstShoot() {
		logger.error("Holy shit! I'm doing the first shot. Wish me well.");
		Players.init(chord);
		Players.updatePlayers(chord);

		shoot(chord);
	}

	private void shoot(ChordImpl chord) {
		ID shootOnId = Shot.selectIdToShootAt(Shot.selectPlayerToShootAt());
		Player meT = Players.me;
		meT.setLastShot(shootOnId);
		Players.savePlayer(meT);

		chord.retrieveAsync(shootOnId);
	}
}
