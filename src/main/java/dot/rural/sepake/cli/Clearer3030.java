package dot.rural.sepake.cli;

import dot.rural.sepake.fuseki.LocalhostFusekiClearer;

public final class Clearer3030 {
    public static void main(final String[] args) {
        clearData();
    }

    private static void log(final String msg) {
        System.out.println(msg); //TODO: Use log4j
    }

    private static void clearData() {
        log("Clearing data...");
        new LocalhostFusekiClearer().clear();
        log("OK, data cleared.");        
    }
}
