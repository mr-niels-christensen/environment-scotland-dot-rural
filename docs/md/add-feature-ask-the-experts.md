Adding a feature: Ask the Experts
=================================

This is a guide to adding a button that takes the user to a question form on http://earthscience.stackexchange.com/ in order to ask a topical question to a forum of experts.

This guide assumes that you already know the diagram "Modify Discover Research Application". The guide tells you how to perform the step "Change files" specifically for adding "Ask the Experts".

## Overview

This button can be made to work entirely on the frontend, i.e. in the user's browser. The feature can be added in two steps:
1. Update the HTML to display an actual button
2. Add some Javascript to make the button work in the intended way

For this feature you will only need to change files in the `src\main\frontend` directory. When you test the changes locally, you will not have to restart the GoogleAppEngineLauncher or the application between updates. Reloading the page in the browser should pick up all changes.

## Step 1: Adding the button, in HTML

I will assume that the button is only needed on the focus page, i.e. the page that shows details and a diagram for one specific paper/person/project. The HTML of the focus page is in the file `src\main\frontend\focus.html`. 
```html
        <div class="summaryRightColumn">
          <div class="ajaxloading"></div>
          <div id="myAjaxAlert" class="alert alert-danger" style="display: none" role="alert">
            We failed to load some of your data. Please try reloading this page, or send an angry email to the developer.
          </div>
          <div id="askPanel" class="smallRightColumnBox">
            <p></p>
            <h2>Ask an expert</h2>
            <p>Ask about
              <i class="labelOfFocus" id="questionText"></i>
            </p>
            <p></p>
            <a role="button" id="askButton" target="_blank" class="btn btn-primary btn-lg btn-block">
               Open question form &nbsp; <span class="glyphicon glyphicon-arrow-right"></span>
            </a>
          </div>
        </div>
```

## Step 2: Making the button active, in Javascript
