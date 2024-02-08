# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_notes.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_notes.robot
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

Scenario: As a site administrator I can add a Notes
  Given a logged-in site administrator
    and an add Notes form
   When I type 'My Notes' into the title field
    and I submit the form
   Then a Notes with the title 'My Notes' has been created

Scenario: As a site administrator I can view a Notes
  Given a logged-in site administrator
    and a Notes 'My Notes'
   When I go to the Notes view
   Then I can see the Notes title 'My Notes'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Notes form
  Go To  ${PLONE_URL}/++add++Notes

a Notes 'My Notes'
  Create content  type=Notes  id=my-notes  title=My Notes

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Notes view
  Go To  ${PLONE_URL}/my-notes
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Notes with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Notes title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
