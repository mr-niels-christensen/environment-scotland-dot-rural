Investigating failures
======================

This document is a small guide to investigating failures in the "Discover Research" application.

* _Server not up (404)_
  - Go to [appengine.google.com](http://appengine.google.com). In the left-side menu under Compute/App Engine check Dashboard, Versions, Settings.
  - If nothing seems wrong in the above but Versions indicate that the system was deployed recently, check [GitHub](https://github.com/mr-niels-christensen/environment-scotland-dot-rural/commits/master) for the latest changes in the code.
* _Missing data in system_
  - Go to [appengine.google.com](http://appengine.google.com). In the left-side menu under Monitoring/Logs change "Any Log Level" to "Error" to see the recent failed actions. Click on any item to see the full logs for that.
  - Go to "/data.html" in the application. After a few seconds, the topmost table ("Data overview") should load a summary of the harvested resources. Along with the logs, this should help you decide which tasks have failed. It is a good idea to keep track of the normal number of resources types in the "Data overview" to clarify if anything is out of the ordinary.
  - If any of the jobs ended with a "Quota Exceeded" failure, see "Account cap reached" below.
  - If the failure seems to be in the search index, you may try to rebuild it by pressing the button "Rebuild Search Index". _Note:_ After clicking the button, nothing will happen for up to a minute. Once the action is done (whether it failed or succeeded), its output is displayed in the frame below the buttons.
  - If the failure seems to be with the data harvesting, you may want to try to revert to yesterday's data by pressing the "Switch defeault/newdata" button. Once the action is done its output is displayed in the frame below the buttons. You should then rebuild the search index as described above.
* _Overnight job failure_
  - See "Missing data in system"
* _API failure, PURE not there_
  - See "Missing data in system"
* _Account cap reached_
  - Go to [appengine.google.com](http://appengine.google.com). In the left-side menu under Compute/App Engine check Dashboard and Quota Details. The latter page has links to documentation explaining resource quotas in details.
* _My paper is not there_
  - First acquire precise details, preferably get a link to the paper on [http://aura.abdn.ac.uk/](http://aura.abdn.ac.uk/) or similar.
  - Try "Missing data in system" above to see if there were any major failures last night.
  - If the paper is relevant and there were no failures, it may be necessary to improve the filters used in `src\main\dotruralsepake\harvest\pure_oai.py` and `src\main\dotruralsepake\harvest\pure_details.py`
