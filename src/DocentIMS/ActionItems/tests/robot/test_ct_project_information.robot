# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_project_information.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_project_information.robot
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

Scenario: As a site administrator I can add a project_information
  Given a logged-in site administrator
    and an add project_information form
   When I type 'My project_information' into the title field
    and I submit the form
   Then a project_information with the title 'My project_information' has been created

Scenario: As a site administrator I can view a project_information
  Given a logged-in site administrator
    and a project_information 'My project_information'
   When I go to the project_information view
   Then I can see the project_information title 'My project_information'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add project_information form
  Go To  ${PLONE_URL}/++add++project_information

a project_information 'My project_information'
  Create content  type=project_information  id=my-project_information  title=My project_information

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the project_information view
  Go To  ${PLONE_URL}/my-project_information
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a project_information with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the project_information title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
