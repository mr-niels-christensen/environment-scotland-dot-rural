	// we will need to set the correct domain for Scolocate, so presumably sepa.local
	document.domain = "environment.scotland.gov.uk"; 

	function errorWebPlayerCallback(errorCode, description) {
		// Displays an error message if something goes wrong in the Web Player.  
	}

	function onWebPlayerOpenedCallback(analysisDocument) {
		// Document is now opened and ready for interactions.  
	}

	function onWebPlayerDocumentClosedCallback(analysisPath) {
		// Document is now closed.  
	}
	
	function layoutWebPlayer(width, height, divName) {
		// Fixes the positioning of the DIV containing the Web Player,
		// must be recalculated for IE6 to work.

		document.getElementById(divName).style.width = width + "px";
		document.getElementById(divName).style.height = height + "px";
	}

        var customisation = new spotfire.webPlayer.Customization();
        customisation.showTopHeader = true;
        customisation.showToolBar = true;
        customisation.showExportFile = true;
        customisation.showExportVisualization = true;
        customisation.showCustomizableHeader = false;
        customisation.showPageNavigation = true;
        customisation.showStatusBar = false;
        customisation.showDodPanel = false;
        customisation.showFilterPanel = false;

    var webPlayer;
	// this address will be changed to be the Scolocate address which should be: http://sgf-sep-app-008.sepa.local/SpotfireWeb
    webPlayer = new spotfire.webPlayer.Application("http://informatics.environment.scotland.gov.uk/SpotfireWeb/", customisation);

    // Register an error handler to catch errors.  
    webPlayer.onError(errorWebPlayerCallback);

    // Register event handler for document opened event.  
    webPlayer.onOpened(onWebPlayerOpenedCallback);

    // Register event handler for document closed event.  
    webPlayer.onClosed(onWebPlayerDocumentClosedCallback);