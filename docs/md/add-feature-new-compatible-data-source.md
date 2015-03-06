Adding a feature: New, fully compatible data source
====================================================

This is a guide to adding a new data source for the "Discover Research" application. In this case, I consider the case where the source is 100% compatible with the existing code. The concrete example is to add projects from the PURE repository of Aarhus University (for which it was easy to find the right URLs).

This guide assumes that you already know the diagram "Modify Discover Research Application". The guide tells you how to perform the step "Change files" specifically for adding a new data source.

## Overview

All data sources are configured in the seed SPARQL file at `src\main\frontend\sparql-backend\seed.sparql.txt`. For this guide you will not need to change any other files. When you test the change locally, you will have to rerun the cron jobs, though. You may actually want to temporarily remove all other data sources and leave in only the new one. That way you will not have to run the Harvest cron job again and again until the new data source is harvested. Do remember to add the remaining data sources back in again!

## Adding a data source, in SPARQL

Open `src\main\frontend\sparql-backend\seed.sparql.txt` and find the section configuring the data source for projcts from the PURE repository of University of Aberdeen:
```SPARQL
#1.b Uni Aberdeen PURE projects
    <http://pure.abdn.ac.uk:8080/ws/rest/getprojectrequest?rendering=xml_long>
      sepake:wasDetailedByCode sepakecode:PureRESTProjectHarvester ;
      foaf:logo "/images/aberdeenunilogo.gif"  .
```

To add the projects from a new university (with a compatible version of PURE), you only need the URL for their PURE repository and the URL of the logo you want to display with their projects. For Aarhus University we will add the following lines:

```SPARQL
    <http://pure.au.dk/ws/rest/getprojectrequest?rendering=xml_long>
      sepake:wasDetailedByCode sepakecode:PureRESTProjectHarvester ;
      foaf:logo <http://www.corpe.et.aau.dk/digitalAssets/52/52278_au-logo.jpg>  .
```

Nothing more is required.
