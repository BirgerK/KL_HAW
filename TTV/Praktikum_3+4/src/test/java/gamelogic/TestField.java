package gamelogic;

import gamelogic.player.Field;
import org.junit.Test;

import java.math.BigInteger;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class TestField {

	@Test
	public void testIsInside() {
		Field fieldNormal = new Field(1, BigInteger.ZERO, BigInteger.TEN, null);
		assertTrue(fieldNormal.isInside(BigInteger.ONE));

		Field fieldBehind = new Field(1, BigInteger.TEN, BigInteger.ONE, null);
		assertTrue(fieldBehind.isInside(BigInteger.ZERO));

		Field fieldFail = new Field(1, BigInteger.ZERO, BigInteger.TEN, null);
		assertFalse(fieldFail.isInside(BigInteger.TEN.add(BigInteger.ONE)));
	}
}
