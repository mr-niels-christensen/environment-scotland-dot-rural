package dot.rural.sepake.pure;

import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.Stack;
import java.util.TreeSet;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public final class PureSaxHandler extends DefaultHandler {
    private static final List<String> IGNORE = Arrays.asList(
            "stab:associatedPublications", "stab:personsUK",
            "stab:associatedActivities",
            "stab:staffOrganisationAssociations",
            "person-template:nameVariants", "person-template:callName");
    private final Set<String> triples = new TreeSet<String>();
    private Stack<String> localNames = new Stack<String>();
    private StringBuffer text = null;
    private String project = null;
    private String dept = null;
    private String person = null;

    public void dump() {
        for (final String triple : triples) {
            System.out.println(triple);
        }
    }

    @Override
    public void startElement(String uri, String localName, String qName,
            Attributes attributes) throws SAXException {
        if ((localNames.size() > 0) && IGNORE.contains(localNames.peek())) {
            return;
        }
        if (IGNORE.contains(qName)) {
            localNames.push(qName);
            return;
        }
        localNames.push(qName);
        text = new StringBuffer();
        if ("core:content".equals(qName)) {
            project = String.format(":Project#%s",
                    attributes.getValue("uuid"));
            triples.add(String.format("%s a prov:Organization", project));
        }
        if ("stab1:owner".equals(qName)) {
            dept = String.format(":Department#%s",
                    attributes.getValue("uuid"));
            triples.add(String.format("%s a prov:Organization", dept));
            triples.add(String.format("%s :owns %s", dept, project));
        }
        if ("person-template:person".equals(qName)) {
            person = String.format(":Person#%s",
                    attributes.getValue("uuid"));
            triples.add(String.format("%s a prov:Person", person));
            triples.add(String.format("%s a foaf:Person", person));
            triples.add(String.format("%s prov:memberOf %s", person,
                    project));
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName)
            throws SAXException {
        if ((localNames.size() > 0) && qName.equals(localNames.peek())) {
            localNames.pop();
        }
        if ((localNames.size() > 0) && IGNORE.contains(localNames.peek())) {
            return;
        }
        String fullText = text.toString().trim();
        if (fullText.length() > 0) {
            if ("stab1:title".equals(qName)) {
                triples.add(String.format("%s rdfs:label \"%s\"", project,
                        fullText));
            }
            if ("organisation-template:name".equals(qName)
                    && (localNames.contains("stab1:owner"))) {
                triples.add(String.format("%s rdfs:label \"%s\"", dept,
                        fullText));
            }
            if ("core:firstName".equals(qName)
                    && (localNames.contains("person-template:person"))) {
                triples.add(String.format("%s foaf:givenName \"%s\"",
                        person, fullText));
            }
            if ("core:lastName".equals(qName)
                    && (localNames.contains("person-template:person"))) {
                triples.add(String.format("%s foaf:familyName \"%s\"",
                        person, fullText));
            }
            if ("person-template:email".equals(qName)
                    && (localNames.contains("person-template:person"))) {
                triples.add(String.format("%s foaf:mbox \"%s\"", person,
                        fullText));
            }
        }
    }

    @Override
    public void characters(char ch[], int start, int length)
            throws SAXException {
        if (IGNORE.contains(localNames.peek())) {
            return;
        }
        text.append(ch, start, length);
    }
}
