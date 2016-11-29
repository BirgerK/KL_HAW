package gamelogic.player;

import java.math.BigInteger;

public class Field {

	private int fieldNumber;
	private BigInteger startHash = null;
	private BigInteger endHash = null;
	private FieldStatus state;

	public Field(int fieldNumber, BigInteger startHash, BigInteger endHash, FieldStatus state) {
		this.fieldNumber = fieldNumber;
		this.startHash = startHash;
		this.endHash = endHash;
		this.state = state;
	}

	public int getFieldNumber() {
		return fieldNumber;
	}

	public void setFieldNumber(int fieldNumber) {
		this.fieldNumber = fieldNumber;
	}

	public BigInteger getStartHash() {
		return startHash;
	}

	public void setStartHash(BigInteger startHash) {
		this.startHash = startHash;
	}

	public BigInteger getEndHash() {
		return endHash;
	}

	public void setEndHash(BigInteger endHash) {
		this.endHash = endHash;
	}

	public FieldStatus getState() {
		return state;
	}

	public void setState(FieldStatus state) {
		this.state = state;
	}

	public boolean isInside(BigInteger field) {
		if (startHash.compareTo(endHash) < 0) {
			return field.compareTo(startHash) > -1 && field.compareTo(endHash) < 1;
		} else {
			return field.compareTo(startHash) > -1 || field.compareTo(endHash) < 1;
		}
	}

	@Override
	public String toString() {
		return "Field{" + "fieldNumber=" + fieldNumber + ", startHash=" + startHash + ", endHash=" + endHash
				+ ", state=" + state + '}';
	}
}
