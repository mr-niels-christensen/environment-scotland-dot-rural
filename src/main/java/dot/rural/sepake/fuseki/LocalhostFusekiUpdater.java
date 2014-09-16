package dot.rural.sepake.fuseki;

public final class LocalhostFusekiUpdater extends FusekiUpdater {
    public LocalhostFusekiUpdater() {
        super("http://localhost:3030/ds/update");
    }
}
