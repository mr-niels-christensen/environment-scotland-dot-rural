package dot.rural.sepake.cli;

import java.io.InputStream;

import javax.xml.parsers.SAXParserFactory;

import dot.rural.sepake.fuseki.FusekiUpdater;
import dot.rural.sepake.pure.PureSaxHandler;

public final class GaeLoader {
    public static void main(final String[] args) {
        loadData();
    }

    private static void log(final String msg) {
        System.out.println(msg); //TODO: Use log4j
    }

    private static void loadData() {
        final String url = String.format("http://%s.appspot.com/ds/query", System.getProperty("app"));
        log(String.format("Data will be POSTed to %s", url));
        final FusekiUpdater fusekiUpdater = new FusekiUpdater(url);
        log("Reading data...");
        try (final InputStream is = GaeLoader.class.getResourceAsStream("all-abdn-projects.xml");)
        {
            SAXParserFactory.newInstance().newSAXParser().parse(is, new PureSaxHandler(fusekiUpdater));
            log("OK, data read. Loading data...");
            fusekiUpdater.flush();
        } catch (final Exception e) {
            throw new RuntimeException(e);
        }
        log("OK, data loaded.");        
    }
}
