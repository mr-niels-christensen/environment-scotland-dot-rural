package dot.rural.sepake.pure;

/*
 * Interface to Collection-like object that accepts triples.
 * Its purpose is make a lightweight facade to an RDF model in Apache Jena.
 */
public interface TripleSink<First, Second, Third> {
    
    /**
     * Add a triple
     * @param first First element in the triple
     * @param second Second element in the triple
     * @param third Third element in the triple
     */
    void addTriple(First first, Second second, Third third);
}
