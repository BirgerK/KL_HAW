package gamelogic;

import de.uniba.wiai.lspi.chord.data.ID;
import gamelogic.player.Field;
import gamelogic.player.Players;

public class Shot {

	public static boolean isBoom(ID target) {
		for (Field f : Players.me.getFields()) {
			if (f.isInside(target.toBigInteger())) {
				return Players.me.isFieldContainingShip(f.getFieldNumber());
			}
		}
		return false;
	}
}
