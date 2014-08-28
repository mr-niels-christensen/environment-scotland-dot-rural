package dot.rural.sepake.cli;

import java.io.InputStream;

import javax.xml.parsers.SAXParserFactory;

import dot.rural.sepake.fuseki.LocalhostFusekiUpdater;
import dot.rural.sepake.pure.PureSaxHandler;

public final class Loader3030 {
    public static void main(final String[] args) {
        loadData();
    }

    private static void log(final String msg) {
        System.out.println(msg); //TODO: Use log4j
    }

    private static void loadData() {
        final LocalhostFusekiUpdater fusekiUpdater = new LocalhostFusekiUpdater();
        log("Reading data...");
        try (final InputStream is = Loader3030.class.getResourceAsStream("search-projects-for-rural.xml");)
        {
            SAXParserFactory.newInstance().newSAXParser().parse(is, new PureSaxHandler(fusekiUpdater));
            log("OK, data read. Loading data into Fuseki...");
            fusekiUpdater.flush();
        } catch (final Exception e) {
            throw new RuntimeException(e);
        }
        log("OK, data loaded.");        
    }
}
