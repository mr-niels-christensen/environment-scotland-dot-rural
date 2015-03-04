environment-scotland-dot-rural
==============================

This project aims to provide a subsite for http://www.environment.scotland.gov.uk/

The purpose of the subsite is to allow the discovery of academic output that is relevant for the portal.

The project requires the following software to be installed:
  * Python 2.7
  * https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
  * pip (if you do not have it, try "easy_install pip")

To run this locally, you need the Python library called "lxml". You may install this directly in your main Python 2.7 installation by typing

    pip install lxml

If you are on a Linux/OSX or such, you will probably need to install as root:

    sudo pip install lxml

If you prefer not to extend the main Python installation with lxml (or you do not have the permissions to do so) you can use a virtual environment:

    virtualenv venv
    source venv/bin/activate
    pip install lxml

Remember to deactivate the virtual environment when working on other projects.

    deactivate

To run the unit test suit, go into the src/main directory and run
    python -m unittest discover -s ../../src/test/python/dot/
    
To run the system locally, type

    dev_appserver.py --log_level=debug src/main/

The website will be available on http://localhost:8080/

The admin console will be available on http://localhost:8000/

To deploy, type

    appcfg.py update src/main/


