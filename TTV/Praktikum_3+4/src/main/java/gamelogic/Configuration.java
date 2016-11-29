package gamelogic;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

public class Configuration {

	private static Map<String, String> configuration = new HashMap<String, String>();

	public static String getProperty(String propertyKey) {
		if (configuration.containsKey(propertyKey)) {
			return configuration.get(propertyKey);
		} else {
			return "";
		}
	}

	public static void init(String propertiesFile) throws IOException {
		Properties properties = new Properties();
		ClassLoader loader = Main.class.getClassLoader();
		properties.load(loader.getResourceAsStream(propertiesFile));
		for (String key : properties.stringPropertyNames()) {
			String value = properties.getProperty(key);
			configuration.put(key, value);
		}
	}
}
