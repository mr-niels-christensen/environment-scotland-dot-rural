package dot.rural.sepake.cli;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.SAXException;

import dot.rural.sepake.fuseki.LocalhostFusekiUpdater;
import dot.rural.sepake.pure.PureSaxHandler;

public final class PutData {
    public static void main(String[] args) throws IOException, SAXException, ParserConfigurationException {
        final LocalhostFusekiUpdater fuseki = new LocalhostFusekiUpdater();
        System.out.println("Reading data...");
        try (final InputStream is = PutData.class.getResourceAsStream("search-projects-for-rural.xml");)
        {
            SAXParserFactory.newInstance().newSAXParser().parse(is, new PureSaxHandler(fuseki));
            System.out.println("OK, data read. Sending data to Fuseki...");
        }
        fuseki.flush();
        System.out.println("OK, data sent.");
    }
}
