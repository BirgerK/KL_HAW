package gamelogic.player;

import de.uniba.wiai.lspi.chord.data.ID;
import gamelogic.Main;

import java.math.BigInteger;
import java.util.*;

public class Player implements Comparable<Player> {

	ID id;
	ID startField;
	int number_of_ships;
	int number_of_fields;

	Set<Integer> fieldNumbersContainingShip = new HashSet<Integer>();
	Map<ID, Boolean> shipWasHitOnField = new HashMap<ID, Boolean>();
	int hitCounter = 0;
	int missCounter = 0;
	ID lastShot = null;

	public Player(ID id, int number_of_ships, int number_of_fields) {
		this.id = id;
		this.number_of_ships = number_of_ships;
		this.number_of_fields = number_of_fields;
	}

	public ID getId() {
		return id;
	}

	public void setId(ID id) {
		this.id = id;
	}

	public ID getStartField() {
		return startField;
	}

	public void setStartField(ID startField) {
		this.startField = startField;
	}

	public int getNumber_of_ships() {
		return number_of_ships;
	}

	public void setNumber_of_ships(int number_of_ships) {
		this.number_of_ships = number_of_ships;
	}

	public int getNumber_of_fields() {
		return number_of_fields;
	}

	public void setNumber_of_fields(int number_of_fields) {
		this.number_of_fields = number_of_fields;
	}

	/**
	 * Errechnet das Start und Endfeld, die Range und wie groß ein jeweiliges Feld ist
	 * @return
	 */
	public List<Field> getFields() {
		List<Field> fields = new ArrayList();
		//Wo beginnt und endet der Bereich eines Spielers
		BigInteger start = this.startField.toBigInteger();
		BigInteger end = this.id.toBigInteger();
		if (start.compareTo(end) > 0) {
			start = start.subtract(Main.MAX_ID);
		}

		//Wie groß ist der Bereich und die einzelnen Felder
		BigInteger idRange = end.subtract(start).add(BigInteger.ONE);
		BigInteger sizeOfField = idRange.divide(BigInteger.valueOf(this.number_of_fields));

		//Die Keys für jedes Feld bestimmen (Start und Ende)
		for (int i = 0; i < this.number_of_fields; i++) {
			BigInteger startField = this.startField.toBigInteger().add(sizeOfField.multiply(BigInteger.valueOf(i)))
					.mod(Main.MAX_ID);
			BigInteger endField = startField.add(sizeOfField).subtract(BigInteger.ONE).mod(Main.MAX_ID);
			Field field = new Field(i, startField, endField, FieldStatus.NOT_TOUCHED);

			for (ID hitId : shipWasHitOnField.keySet()) {
				if (field.isInside(hitId.toBigInteger())) {
					if (field.getState().equals(FieldStatus.NOT_TOUCHED)) {
						field.setState(getFieldStatus(hitId));
					} else if (!field.getState().equals(FieldStatus.NOT_SURE)) {
						FieldStatus newStatus = getFieldStatus(hitId);
						if (!newStatus.equals(field.getState())) {
							field.setState(FieldStatus.NOT_SURE);
						}
					}
				}
			}

			fields.add(field);
		}

		return fields;
	}

	/**
	 * Gibt an ob das Feld
	 * @param id des Feldes
	 * @return
	 */
	private FieldStatus getFieldStatus(ID id) {
		if (shipWasHitOnField.containsKey(id)) {
			if (shipWasHitOnField.get(id)) {
				return FieldStatus.HIT;
			} else {
				return FieldStatus.MISSED;
			}
		} else {
			return FieldStatus.NOT_TOUCHED;
		}
	}


	public Set<Integer> getFieldNumbersContainingShip() {
		return fieldNumbersContainingShip;
	}

	public void setFieldNumbersContainingShip(Set<Integer> fieldNumbersContainingShip) {
		this.fieldNumbersContainingShip = fieldNumbersContainingShip;
	}

	public boolean isFieldContainingShip(int fieldNumber) {
		return fieldNumbersContainingShip.contains(fieldNumber);
	}

	/**
	 * Player did shoot on field
	 *
	 * @param field welches Feld auf das geschossen wurde
	 * @param hit wurde das Feld getroffen (1) nicht getroffen (0)
	 */
	public void shotAtField(ID field, boolean hit) {
		if (hit) {
			hitCounter++;
		} else {
			missCounter++;
		}
		this.shipWasHitOnField.put(field, hit);
	}

	public Map<ID, Boolean> getShipWasHitOnField() {
		return shipWasHitOnField;
	}

	public void setShipWasHitOnField(Map<ID, Boolean> shipWasHitOnField) {
		this.shipWasHitOnField = shipWasHitOnField;
	}

	public ID getLastShot() {
		return lastShot;
	}

	public void setLastShot(ID lastShot) {
		this.lastShot = lastShot;
	}

	public int getHitCounter() {
		return hitCounter;
	}

	public int getMissCounter() {
		return missCounter;
	}

	public int getRemainingShips() {
		return number_of_ships - getHitCounter();
	}

	public boolean isDefeated() {
		return getRemainingShips() <= 0;
	}

	@Override
	public int compareTo(Player o) {
		return this.getId().compareTo(o.getId());
	}

	@Override
	public boolean equals(Object o) {
		if (this == o)
			return true;
		if (o == null || getClass() != o.getClass())
			return false;

		Player player = (Player) o;

		return id.equals(player.id);

	}

	@Override
	public int hashCode() {
		return id.hashCode();
	}

	@Override
	public String toString() {
		return "Player{" + "id=" + id + ", startField=" + startField + ", number_of_ships=" + number_of_ships
				+ ", number_of_fields=" + number_of_fields + ", fieldNumbersContainingShip="
				+ fieldNumbersContainingShip + ", shipWasHitOnField=" + shipWasHitOnField + ", lastShot=" + lastShot
				+ '}';
	}
}
