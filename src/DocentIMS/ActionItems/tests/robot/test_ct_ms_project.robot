# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_ms_project.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_ms_project.robot
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

Scenario: As a site administrator I can add a ms_project
  Given a logged-in site administrator
    and an add ms_project form
   When I type 'My ms_project' into the title field
    and I submit the form
   Then a ms_project with the title 'My ms_project' has been created

Scenario: As a site administrator I can view a ms_project
  Given a logged-in site administrator
    and a ms_project 'My ms_project'
   When I go to the ms_project view
   Then I can see the ms_project title 'My ms_project'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add ms_project form
  Go To  ${PLONE_URL}/++add++ms_project

a ms_project 'My ms_project'
  Create content  type=ms_project  id=my-ms_project  title=My ms_project

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the ms_project view
  Go To  ${PLONE_URL}/my-ms_project
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a ms_project with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the ms_project title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
