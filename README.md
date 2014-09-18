environment-scotland-dot-rural
==============================

This project aims to provide a backend service for http://www.environment.scotland.gov.uk/

The purpose of the service is to allow the discovery of academic output that is relevant for the portal.

This project currently requires 
  * Java 1.7+
  * Gradle. 
  * python 2.7+
  * pip
  * virtualenv
  * make
    
Open two prompts.
Type
```
gradle fuseki
```
in one of them and verify that the Fuseki starts up with some log4j warnings (this is work-in-progress...)
In the other, type
```
gradle run
```
and watch the application load data into Fuseki, then end. Type
```
make
```
and wait for that application to load more data into Fuseki.

Now point a browser at `build/www/index.html`
