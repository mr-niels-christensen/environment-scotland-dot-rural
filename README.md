environment-scotland-dot-rural
==============================

This project aims to provide a backend service for http://www.environment.scotland.gov.uk/

The purpose of the service is to allow the discovery of academic output that is relevant for the portal.

This project requires Java 1.7+ and Gradle. The build scripts are work-in-progress. When Java and Gradle are installed, open two prompts.
Type
```
gradle fuseki
```
in one of them and verify that the Fuseki starts up with some log4j warnings (yeah, work-in-progress...)
```
gradle run
```
and watch the application load data into Fuseki, then end.

Now point a browser at `build/www/index.html`
