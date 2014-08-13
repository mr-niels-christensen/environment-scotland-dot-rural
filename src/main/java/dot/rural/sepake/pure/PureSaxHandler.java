package dot.rural.sepake.pure;

import java.util.Arrays;
import java.util.List;
import java.util.Stack;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

/**
 * A SAX handler that generates RDF triples from the output of
 * the REST interface of Elsevier PURE version 4.
 * 
 * A PureSaxHandler acts as a Director in the Builder pattern.
 * The Builder is a TripleSink<String, String, String>
 */
public final class PureSaxHandler extends DefaultHandler {
    /** These tags contain data that we currently do not need */
    private static final List<String> IGNORE = Arrays.asList(
            "stab:associatedPublications", "stab:personsUK",
            "stab:associatedActivities",
            "stab:staffOrganisationAssociations",
            "person-template:nameVariants", "person-template:callName");
    /** Parsed triples will be added to this object. */
    private final TripleSink<String, String, String> triples;
    /** Records the currently open tags during parsing */
    private Stack<String> localNames = new Stack<String>();
    /** Records all characters seen since last tag close */
    private StringBuffer text = null;
    /** If a project is currently begin parsed, this records its RDF identifier */
    private String project = null;
    /** If a department is currently begin parsed, this records its RDF identifier */
    private String dept = null;
    /** If a person is currently begin parsed, this records its RDF identifier */
    private String person = null;
    
    /**
     * Registers the Builder object.
     * @param tripleSink Parsed triples will be added to this object.
     */
    public PureSaxHandler(final TripleSink<String, String, String> tripleSink) {
        this.triples = tripleSink;
    }
    
    @Override
    public void startElement(String uri, String localName, String qName,
            Attributes attributes) throws SAXException {
        //Skip processing if we're inside an ignored tag
        if ((localNames.size() > 0) && IGNORE.contains(localNames.peek())) {
            return;
        }
        //Skip processing if we encounter an ignored tag
        if (IGNORE.contains(qName)) {
            localNames.push(qName);
            return;
        }
        //Update parser fields
        localNames.push(qName);
        text = new StringBuffer();
        if ("core:content".equals(qName)) {// This defines a new project
            project = String.format("<Project#%s>",
                    attributes.getValue("uuid"));
            triples.addTriple(project, "rdf:type", "prov:Organization");
        }
        if ("stab1:owner".equals(qName)) {// This defines a new department
            dept = String.format("<Department#%s>",
                    attributes.getValue("uuid"));
            triples.addTriple(dept, "rdf:type", "prov:Organization");
            triples.addTriple(dept, "<owns>", project);
        }
        if ("person-template:person".equals(qName)) {// This defines a new person
            person = String.format("<Person#%s>",
                    attributes.getValue("uuid"));
            triples.addTriple(person, "rdf:type", "prov:Person");
            triples.addTriple(person, "rdf:type", "foaf:Person");
            triples.addTriple(person, "prov:memberOf", project);
        }
    }

    @Override
    public void endElement(String uri, String localName, String qName)
            throws SAXException {
        //Update tag stack
        if ((localNames.size() > 0) && qName.equals(localNames.peek())) {
            localNames.pop();
        }
        //Skip processing if we're inside an ignored tag
        if ((localNames.size() > 0) && IGNORE.contains(localNames.peek())) {
            return;
        }
        //Update parser field
        String fullText = text.toString().trim();
        if (fullText.length() > 0) {// If there was actual text, use it if the tag was relevant
            fullText = String.format("'%s'", fullText);//Quote as SPARQL constant
            if ("stab1:title".equals(qName)) {// Title of a project
                triples.addTriple(project, "rdfs:label", fullText);
            }
            if ("organisation-template:name".equals(qName)
                    && (localNames.contains("stab1:owner"))) {// Name of a department
                triples.addTriple(dept, "rdfs:label", fullText);
            }
            if ("core:firstName".equals(qName)
                    && (localNames.contains("person-template:person"))) {// Name of a person
                triples.addTriple(person, "foaf:givenName", fullText);
            }
            if ("core:lastName".equals(qName)
                    && (localNames.contains("person-template:person"))) {// Name of a person
                triples.addTriple(person, "foaf:familyName", fullText);
            }
            if ("person-template:email".equals(qName)
                    && (localNames.contains("person-template:person"))) {// Email of a person
                triples.addTriple(person, "foaf:mbox", fullText);
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
