environment-scotland-dot-rural
==============================

This project aims to provide a backend service for http://www.environment.scotland.gov.uk/

The purpose of the service is to allow the discovery of academic output that is relevant for the portal.

The project requires the following software to be installed:
  * https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
  * Python 2.7
  * pip (if you do not have it, try "easy_install pip"
  * make
  * curl (TODO: remove this dependency, only used for downloading a pip package from github)
  
Running "make" in the project root should download all required python packages, link them into the source appropriately and launch a local server on port 8080.

