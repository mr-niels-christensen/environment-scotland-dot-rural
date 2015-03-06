Adding a feature: Ask the Experts
=================================

This is a guide to adding a button that takes the user to a question form on `http://earthscience.stackexchange.com/` in order to ask a topical question to a forum of experts.

This guide assumes that you already know the diagram "Modify Discover Research Application". The guide tells you how to perform the step "Change files" specifically for adding "Ask the Experts".

## Overview

This button can be made to work entirely on the frontend, i.e. in the user's browser. The feature can be added in two steps:
1. Update the HTML to display an actual button
2. Add some JavaScript to make the button work in the intended way

For this feature you will only need to change files in the `src\main\frontend` directory. When you test the changes locally, you will not have to restart the GoogleAppEngineLauncher or the application between updates. Reloading the page in the browser should pick up all changes.

## Step 1: Adding the button, in HTML

I will assume that the button is only needed on the focus page, i.e. the page that shows details and a diagram for one specific paper/person/project. The HTML of the focus page is in the file `src\main\frontend\focus.html`. 

To find the code that defines the meat of the page, search for the first comment containing the text `BEGIN app-specific code`. That's where the header and search bar code ends. The HTML from there until the comment `END app-specific code` builds the summary, the diagram and the (mostly empty) column to the right of these.

I will place the button on a panel in that right-hand column. The column is not quite empty; it contains room for displaying the spinning "data is loading" icon as well as an error message in case the server fails to some of the requested data. At the time of writing, the HTML for the column has this layout:
```html
        <div class="summaryRightColumn">
          <div class="ajaxloading"></div>
          <div id="myAjaxAlert" class="alert alert-danger" style="display: none" role="alert">
            ...some error message...
          </div>
        </div>
```

Our new panel and button should be inserted after the `div` with id `myAjaxAlert` to make it appear beneath the spinner and the potential error message, like this:
```html
        <div class="summaryRightColumn">
          <div class="ajaxloading"></div>
          <div id="myAjaxAlert" class="alert alert-danger" style="display: none" role="alert">
            ...some error message...
          </div>
          <div id="askPanel" class="smallRightColumnBox">
            <p></p>
            <h2>Ask an expert</h2>
            <p></p>
            <a role="button" id="askButton" target="_blank" class="btn btn-primary btn-lg btn-block">
               Open question form &nbsp; <span class="glyphicon glyphicon-arrow-right"></span>
            </a>
          </div>
        </div>
```

So far so good. If you test the updated application locally (as described in the diagram "Test application locally"), the button should appear, but it still does nothing when clicked.

## Step 2: Making the button active, in JavaScript

I want the button to open a partially filled question form on `http://earthscience.stackexchange.com/`. I want the title of paper on the focus page to be filled in, and I want the question to be tagged "environment" and "scotland". Through trial and error I have established that for a paper named "Sunshine", the URL should be `http://earthscience.stackexchange.com/questions/ask?tags=environment scotland&title=Sunshine`

Create a new JavaScript file `src\main\frontend\focus-ask.js`. The convention for our JavaScript files is to indicate the "owning" HTML page before the hyphen. In this case the code supports `focus.html` so I put `focus` before `ask`. Shared JavaScript files begin with `common`.

Put the following code in the file:
```javascript
$( document ).ready( function() {
  $( "#askButton" ).click(function() {
    var url = encodeURI(
        'http://earthscience.stackexchange.com/questions/ask?tags=environment scotland&title=' 
        + $( '#focusPanel .focusLabel' ).text()
    );
    $( this ).attr( "href", url );//Go to the url
  });
});
```

If you compare the URL I gave above, you can see that the title (Sunshine) is acquired using the jQuery expression `$( '#focusPanel .focusLabel' ).text()`. This expression reads the content of an `h2` heading created by the code in `src\main\frontend\focus-description.js`. The heading is the one you acutally see on the focus page.

All you now need to do is to include the new JavaScript file in `src\main\frontend\focus.html`. Open the file and find this import:
```html
<script src="focus-description.js"></script>
```

Insert this import after the above:
```html
<script src="focus-ask.js"></script>
```

The button should now be fully functional!
