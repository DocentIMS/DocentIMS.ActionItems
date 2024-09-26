# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_meeting_notes.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_meeting_notes.robot
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

Scenario: As a site administrator I can add a Meeting Notes
  Given a logged-in site administrator
    and an add Meeting Notes form
   When I type 'My Meeting Notes' into the title field
    and I submit the form
   Then a Meeting Notes with the title 'My Meeting Notes' has been created

Scenario: As a site administrator I can view a Meeting Notes
  Given a logged-in site administrator
    and a Meeting Notes 'My Meeting Notes'
   When I go to the Meeting Notes view
   Then I can see the Meeting Notes title 'My Meeting Notes'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Meeting Notes form
  Go To  ${PLONE_URL}/++add++Meeting Notes

a Meeting Notes 'My Meeting Notes'
  Create content  type=Meeting Notes  id=my-meeting_notes  title=My Meeting Notes

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Meeting Notes view
  Go To  ${PLONE_URL}/my-meeting_notes
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Meeting Notes with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Meeting Notes title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
