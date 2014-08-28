package dot.rural.sepake.fuseki;

import java.util.Scanner;
import com.hp.hpl.jena.update.UpdateExecutionFactory;
import com.hp.hpl.jena.update.UpdateFactory;
import com.hp.hpl.jena.update.UpdateProcessor;

public final class LocalhostFusekiClearer {
    private final String SPARUL_CLEAR_STRING = 
            new Scanner(getClass().getResourceAsStream("sparul-clear-string.txt"), "UTF-8")
                .useDelimiter("\\A")
                .next();

    public void clear() {
        UpdateProcessor upp = UpdateExecutionFactory.createRemote(
                UpdateFactory.create(SPARUL_CLEAR_STRING), 
                "http://localhost:3030/ds/update");
        upp.execute();
    }

}
