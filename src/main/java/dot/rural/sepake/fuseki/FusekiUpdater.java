package dot.rural.sepake.fuseki;

import java.io.Flushable;
import java.io.IOException;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

import com.hp.hpl.jena.update.UpdateExecutionFactory;
import com.hp.hpl.jena.update.UpdateFactory;
import com.hp.hpl.jena.update.UpdateProcessor;

import dot.rural.sepake.pure.TripleSink;

public final class FusekiUpdater implements
        TripleSink<String, String, String>,
        Flushable {
	
	private String url;

	public FusekiUpdater(final String url) {
		this.url = url;
	}
    private final String sparulFormatString = 
            new Scanner(getClass().getResourceAsStream("sparul-format-string.txt"), "UTF-8")
                .useDelimiter("\\A")
                .next();
    private final Set<String> triples = new HashSet<String>();
    
    public void addTriple(String object, String predicate, String subject) {
        this.triples.add(String.format("%s %s %s .\n", object, predicate, subject));
    }

    public void flush() throws IOException {
        if (this.triples.size() > 0) {
            final StringBuffer stmts = new StringBuffer();
            for (final String triple : this.triples) {
                stmts.append(triple);
            }
            final String updateRequest = String.format(this.sparulFormatString, stmts);
            try {
                UpdateProcessor upp = UpdateExecutionFactory.createRemote(
                        UpdateFactory.create(updateRequest), 
                        this.url);
                upp.execute();
            } catch (RuntimeException e) {
                System.err.println("Exception occurred while performing the following SPARQL query.");
                final String[] sparqlSplit = updateRequest.split("\\n");
                for (int i = 0; i < sparqlSplit.length; i++) {
                    System.err.println(String.format("<%4d>%s", i + 1, sparqlSplit[i]));
                }
                throw e;
            }
            triples.clear();
        }
    }

    @Override
    public void addTriple(String object, String predicate, String subject,
            String xsdType) {
        subject = subject.replace('\'', '\"').replace('\n', ' ');//TODO: Better encoding handling
        if (null != xsdType) {
            this.triples.add(String.format("%s %s '%s'^^%s .\n", object, predicate, subject, xsdType));
        } else {
            this.triples.add(String.format("%s %s '%s' .\n", object, predicate, subject));            
        }
        
    }

}
