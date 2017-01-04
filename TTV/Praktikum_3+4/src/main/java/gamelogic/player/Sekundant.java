package gamelogic.player;

import java.util.Comparator;
import java.util.Random;

public class Sekundant implements Comparator<Player> {

	@Override
	public int compare(Player o1, Player o2) {
		if (o1.getHitCounter() > o2.getHitCounter()) {//1.Nr of hits
			return -1;
		} else if (o2.getHitCounter() > o1.getHitCounter()) {
			return 1;
		} else {
			if (o1.getMissCounter() > o2.getMissCounter()) {//2. Nr of hit fields
				return -1;
			} else if (o2.getMissCounter() > o1.getMissCounter()) {
				return 1;
			} else {// 3. Anyone
				Random random = new Random();
				boolean randomness = random.nextBoolean();
				if (randomness) {
					return -1;
				} else {
					return 1;
				}
			}
		}
	}

}
