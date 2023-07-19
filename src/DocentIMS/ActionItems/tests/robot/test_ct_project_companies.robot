# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_project_companies.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_project_companies.robot
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

Scenario: As a site administrator I can add a project_companies
  Given a logged-in site administrator
    and an add project_companies form
   When I type 'My project_companies' into the title field
    and I submit the form
   Then a project_companies with the title 'My project_companies' has been created

Scenario: As a site administrator I can view a project_companies
  Given a logged-in site administrator
    and a project_companies 'My project_companies'
   When I go to the project_companies view
   Then I can see the project_companies title 'My project_companies'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add project_companies form
  Go To  ${PLONE_URL}/++add++project_companies

a project_companies 'My project_companies'
  Create content  type=project_companies  id=my-project_companies  title=My project_companies

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the project_companies view
  Go To  ${PLONE_URL}/my-project_companies
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a project_companies with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the project_companies title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
