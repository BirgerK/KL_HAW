/*
 * Added by INET
 */
package de.uniba.wiai.lspi.chord.service;

import de.uniba.wiai.lspi.chord.data.ID;

public interface NotifyCallback {

	void retrieved(ID target);

	void broadcast(ID source, ID target, Boolean hit, int transactionNumber);

}
