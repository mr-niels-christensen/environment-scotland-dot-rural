The Discover Research application: Getting started
==================================================

This guide is a list of technologies and guides related to the Discover Research application.

## Code

The code resides GitHub using the `git` version control system, see
- http://readwrite.com/2013/09/30/understanding-github-a-journey-for-beginners-part-1

The server code is written in Python 2.7, see
- https://docs.python.org/2/tutorial/

The client code is written in HTML, JavaScript and CSS, see
- http://www.w3schools.com/

## Servers

The application is deployed on Google App Engine (also known as GAE), which is part of the Google Cloud offering. There are no actual, real, physical, named servers. On GAE, one names a "project" and upload"s code to that project. The administrator uses a web interface to set up the "amount of server power" to use for the application. The same web interface gives access to logging and monitoring tools. See
- https://cloud.google.com/appengine/docs

## Documentation

All documentation can be found in [the `docs` directory on GitHub](https://github.com/mr-niels-christensen/environment-scotland-dot-rural/tree/master/docs)

The above link also describes how to export or modify the guides and diagrams.

### Diagrams

There are diagrams explaining the deployment and operation of the system, see
- https://github.com/mr-niels-christensen/environment-scotland-dot-rural/tree/master/docs/pdf

The best place to begin is `deploy-app-from-scratch.pdf`

This describes a "completely new beginning", starting from a machine with no special software installed, ending with the deployment of our module running in a newly created application on Google App Engine (GAE).

The other three diagrams describe important parts of that process.

`setup-github-python-gae.pdf` describes how to install the tools needed to modify/test/deploy the application. This should only be required once per machine.

`modify-application.pdf` describes the process for modifying an existing deployment, assuming the tools have been installed.

`test-application-locally.pdf` describes how to test changes before deploying them. The main reason for a separate process is that the test-server does not run cron jobs automatically, so a bit of button-presseing is required to get some test data into the local version of the application.

`cron-sequence.pdf` describes the nightly cron jobs in sequence and how each one affects the application’s data.

`apis-and-protocols.pdf` describes the data exchanges that the applications takes part of (with the user and with 3rd-party data sources).

`functional-diagram.pdf` is an overview of implemented and planned functionalities.

`functional-diagram-annotated.pdf` is the above with each functionality annotated with the best file to start with when revising the feature. A "map to the code", so to speak.

### Guides

We have created a number of guides on development and operational tasks.

_Investigating failures_: Failure scenarios are discussed in https://github.com/mr-niels-christensen/environment-scotland-dot-rural/blob/master/docs/md/investigating-failures.md

_Generate a custom report_: The application can be queried using the SPARQL language, see https://github.com/mr-niels-christensen/environment-scotland-dot-rural/blob/master/docs/md/generate-custom-report.md

_Adding a frontend feature_ is described with the example of an "Ask the Expert" button here: https://github.com/mr-niels-christensen/environment-scotland-dot-rural/blob/master/docs/md/add-feature-ask-the-experts.md
This guide should also be useful if you need to adjust other frontend features, like improving the design of components.

_Adding a feature: New, fully compatible data source_: This is an example of how to work with the modular, SPARQL-based harvesting system: https://github.com/mr-niels-christensen/environment-scotland-dot-rural/blob/master/docs/md/add-feature-new-compatible-data-source.md

_Extending the refined search_: Explained in https://github.com/mr-niels-christensen/environment-scotland-dot-rural/blob/master/docs/md/add-item-refine-search.md

`reset-metrics`: How to remove all existing metrics and start from scratch. This may be useful when going from a test phase into a production phase, in case the test metrics are not desirable.

### Development blog

Some of the underlying technologies have been discussed in blog posts on https://semanticwebrecipes.wordpress.com/

The posts most relevant to the final Discover Research application are:
- A note on the diagram technology used (Google Visualization OrgChart): https://semanticwebrecipes.wordpress.com/2014/07/24/accessing-linked-data-api-with-javascript/
- How missing descriptions of items can be loaded from Wikipedia: https://semanticwebrecipes.wordpress.com/2014/10/24/add-a-description-using-jquery-and-dbpedia-lookup/
- How RDF graphs was implemented on Google App Engine: https://semanticwebrecipes.wordpress.com/2015/01/09/triple-store-in-the-cloud/

