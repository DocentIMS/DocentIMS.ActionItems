# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_sow_analysis.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_sow_analysis.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Sow Analysis
  Given a logged-in site administrator
    and an add Sow Analysis form
   When I type 'My Sow Analysis' into the title field
    and I submit the form
   Then a Sow Analysis with the title 'My Sow Analysis' has been created

Scenario: As a site administrator I can view a Sow Analysis
  Given a logged-in site administrator
    and a Sow Analysis 'My Sow Analysis'
   When I go to the Sow Analysis view
   Then I can see the Sow Analysis title 'My Sow Analysis'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Sow Analysis form
  Go To  ${PLONE_URL}/++add++Sow Analysis

a Sow Analysis 'My Sow Analysis'
  Create content  type=Sow Analysis  id=my-sow_analysis  title=My Sow Analysis

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Sow Analysis view
  Go To  ${PLONE_URL}/my-sow_analysis
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Sow Analysis with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Sow Analysis title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
