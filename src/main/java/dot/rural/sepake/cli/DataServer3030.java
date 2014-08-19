package dot.rural.sepake.cli;

import java.io.InputStream;

import javax.xml.parsers.SAXParserFactory;

import org.apache.jena.fuseki.EmbeddedFusekiServer;

import dot.rural.sepake.fuseki.LocalhostFusekiUpdater;
import dot.rural.sepake.pure.PureSaxHandler;

public final class DataServer3030 {
    private static final EmbeddedFusekiServer FUSEKI = EmbeddedFusekiServer.mem(3030, "/ds");
    private static Thread FUSEKI_CLOSER = new Thread() {
        public void run() { 
            FUSEKI.stop();
            log("Stopped");
        }
    };
    
    public static void main(final String[] args) {
        FUSEKI.start();
        Runtime.getRuntime().addShutdownHook(FUSEKI_CLOSER);
        loadData();
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            log("Stopping...");
        }
    }

    private static void log(final String msg) {
        System.out.println(msg); //TODO: Use log4j
    }

    private static void loadData() {
        final LocalhostFusekiUpdater fusekiUpdater = new LocalhostFusekiUpdater();
        log("Reading data...");
        try (final InputStream is = DataServer3030.class.getResourceAsStream("search-projects-for-rural.xml");)
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
