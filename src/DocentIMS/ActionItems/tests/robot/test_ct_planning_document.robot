# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_planning_document.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_planning_document.robot
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

Scenario: As a site administrator I can add a Planning Document
  Given a logged-in site administrator
    and an add Planning Document form
   When I type 'My Planning Document' into the title field
    and I submit the form
   Then a Planning Document with the title 'My Planning Document' has been created

Scenario: As a site administrator I can view a Planning Document
  Given a logged-in site administrator
    and a Planning Document 'My Planning Document'
   When I go to the Planning Document view
   Then I can see the Planning Document title 'My Planning Document'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Planning Document form
  Go To  ${PLONE_URL}/++add++Planning Document

a Planning Document 'My Planning Document'
  Create content  type=Planning Document  id=my-planning_document  title=My Planning Document

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Planning Document view
  Go To  ${PLONE_URL}/my-planning_document
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Planning Document with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Planning Document title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
