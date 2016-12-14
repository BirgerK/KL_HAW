package gamelogic;

import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.util.logging.Logger;
import gamelogic.player.*;

import java.math.BigInteger;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class Shot {

	private static Logger logger = Logger.getLogger(Shot.class);

	public static boolean isBoom(ID target) {
		for (Field f : Players.me.getFields()) {
			if (f.isInside(target.toBigInteger())) {
				return Players.me.isFieldContainingShip(f.getFieldNumber());
			}
		}
		return false;
	}

	public static Player selectPlayerToShootAt() {
		logger.info("Selecting next player to shoot at.");
		Player result = null;

		List<Player> allPlayers = Players.getAll();
		Collections.sort(allPlayers, new Sekundant());

		for (Player player : allPlayers) {
			if (!player.equals(Players.me)) { // get first player, which is not ME
				result = player;
				break;
			}
		}

		logger.info("Selected player " + result + " to shoot at next time.");
		return result;
	}

	public static ID selectIdToShootAt(Player player) {
		ID result = null;

		Random random = new Random();

		if (player != null) { // if a player was found
			List<Field> playerFields = player.getFields();
			List<Field> unusedFields = playerFields.stream()
					.filter(field -> field.getState().equals(FieldStatus.NOT_TOUCHED)).collect(Collectors.toList());
			if (!unusedFields.isEmpty()) {
				Field field = unusedFields.get(random.nextInt(unusedFields.size()));
				result = ID.valueOf(calcMiddle(field.getStartHash(), field.getEndHash()));
			}
		}

		if (player == null
				|| result == null) { // if no player was found to shoot at, take a random field which is not MINE
			BigInteger selfStart = Players.me.getStartField().toBigInteger();
			BigInteger selfEnd = Players.me.getId().toBigInteger();
			BigInteger fieldNrToShootAt = BigInteger.ZERO;
			while (fieldNrToShootAt.compareTo(selfStart) < 0 && fieldNrToShootAt.compareTo(selfEnd) > 0) {
				fieldNrToShootAt = new BigInteger(Main.NR_BITS_ID, random);
			}
			result = ID.valueOf(fieldNrToShootAt);
		}

		return result;
	}

	private static BigInteger calcMiddle(BigInteger from, BigInteger to) {
		if (from.compareTo(to) < 0) {
			return from.add(to).divide(BigInteger.valueOf(2)).mod(Main.MAX_ID);
		} else if (from.compareTo(to) > 0) {
			return from.add(to.add(Main.MAX_ID)).divide(BigInteger.valueOf(2)).mod(Main.MAX_ID);
		} else {
			return from;
		}
	}
}
