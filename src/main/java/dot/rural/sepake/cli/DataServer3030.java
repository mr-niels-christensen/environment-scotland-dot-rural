package dot.rural.sepake.cli;

import org.apache.jena.fuseki.EmbeddedFusekiServer;

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
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            log("Stopping...");
        }
    }

    private static void log(final String msg) {
        System.out.println(msg); //TODO: Use log4j
    }
}
