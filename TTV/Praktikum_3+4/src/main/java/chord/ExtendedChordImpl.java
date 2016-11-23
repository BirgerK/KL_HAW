package chord;

import de.uniba.wiai.lspi.chord.data.ID;
import de.uniba.wiai.lspi.chord.service.impl.ChordImpl;

public class ExtendedChordImpl extends ChordImpl {

	public void broadcast (ID target, Boolean hit) {
		this.logger.debug("App called broadcast");

	}


}
