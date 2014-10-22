environment-scotland-dot-rural
==============================

This project aims to provide a backend service for http://www.environment.scotland.gov.uk/

The purpose of the service is to allow the discovery of academic output that is relevant for the portal.

This project currently requires 
  * python 2.7+
  * pip
  * virtualenv
  * make
  * a SPARQL endpoint (see below)
  
Including a SPARQL endpoint is work in progress.
Until then I suggest installing Fuseki and running

```
./fuseki-server -v --update --mem /ds
```

This will start an empty Fuseki on localhost:3030

Then run
```
make
```
and watch the application load data into Fuseki.

Now point a browser at `src/main/frontend/index.html`
