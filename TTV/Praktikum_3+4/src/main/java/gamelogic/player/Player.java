package gamelogic.player;

import de.uniba.wiai.lspi.chord.data.ID;

import java.util.*;

public class Player implements Comparable<Player> {

	ID id;
	ID startField;
	int number_of_ships;
	int number_of_fields;

	List<Field> fields = new ArrayList();
	Set<Integer> fieldNumbersContainingShip = new HashSet<Integer>();
	Map<ID, Boolean> shipWasHitOnField = new HashMap<ID, Boolean>();

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

	public List<Field> getFields() {
		return fields;
	}

	public void setFields(List<Field> fields) {
		this.fields = fields;
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

	//TODO: rename it! (Es wurde ein Schiff auf Feld x beschossen, und das muss der Player sich merken!)
	public void addShotShipOnField(ID field, boolean hit) {
		this.shipWasHitOnField.put(field, hit);
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
}
