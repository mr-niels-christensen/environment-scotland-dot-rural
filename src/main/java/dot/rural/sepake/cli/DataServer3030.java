package dot.rural.sepake.cli;

import org.apache.jena.fuseki.EmbeddedFusekiServer;
import org.apache.metamodel.DataContext;
import org.apache.metamodel.QueryPostprocessDataContext;
import org.apache.metamodel.schema.Column;
import org.apache.metamodel.schema.Schema;
import org.apache.metamodel.schema.Table;
import org.apache.metamodel.xml.XmlDomDataContext;

public final class DataServer3030 {
    private static final EmbeddedFusekiServer FUSEKI = EmbeddedFusekiServer.mem(3030, "/ds");
    private static Thread FUSEKI_CLOSER = new Thread() {
        public void run() { 
            FUSEKI.stop();
            log("Stopped");
        }
    };
    
    public static void main(final String[] args) {
        metamodel();
        FUSEKI.start();
        Runtime.getRuntime().addShutdownHook(FUSEKI_CLOSER);
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            log("Stopping...");
        }
    }

    private static void metamodel() {
        // a DataContext for an XML file (where metadata is automatically inferred)
        DataContext dataContext = new XmlDomDataContext(DataServer3030.class.getResource("search-projects-for-rural.xml"), true); 
        Schema[] schemas = dataContext.getSchemas();  
        log("Schemas");
        for (final Schema s : schemas) {
            log(s.toString());
        }
        Table[] tables = schemas[1].getTables();  
        log("Tables");
        for (final Table s : tables) {
            log(s.toString());
        }
        Column[] columns = tables[1].getColumns();
        log("Columns");
        for (final Column s : columns) {
            log(s.toString());
        }
        QueryPostprocessDataContext t;
    }
    
    private static void log(final String msg) {
        System.out.println(msg); //TODO: Use log4j
    }
}
