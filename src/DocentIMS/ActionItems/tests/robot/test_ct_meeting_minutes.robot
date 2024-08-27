# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_meeting_minutes.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_meeting_minutes.robot
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

Scenario: As a site administrator I can add a Meeting Minutes
  Given a logged-in site administrator
    and an add Meeting Minutes form
   When I type 'My Meeting Minutes' into the title field
    and I submit the form
   Then a Meeting Minutes with the title 'My Meeting Minutes' has been created

Scenario: As a site administrator I can view a Meeting Minutes
  Given a logged-in site administrator
    and a Meeting Minutes 'My Meeting Minutes'
   When I go to the Meeting Minutes view
   Then I can see the Meeting Minutes title 'My Meeting Minutes'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Meeting Minutes form
  Go To  ${PLONE_URL}/++add++Meeting Minutes

a Meeting Minutes 'My Meeting Minutes'
  Create content  type=Meeting Minutes  id=my-meeting_minutes  title=My Meeting Minutes

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Meeting Minutes view
  Go To  ${PLONE_URL}/my-meeting_minutes
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Meeting Minutes with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Meeting Minutes title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
