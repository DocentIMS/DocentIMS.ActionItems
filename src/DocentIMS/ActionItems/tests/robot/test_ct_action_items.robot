# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_action_items.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_action_items.robot
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

Scenario: As a site administrator I can add a Action Items
  Given a logged-in site administrator
    and an add Action Items form
   When I type 'My Action Items' into the title field
    and I submit the form
   Then a Action Items with the title 'My Action Items' has been created

Scenario: As a site administrator I can view a Action Items
  Given a logged-in site administrator
    and a Action Items 'My Action Items'
   When I go to the Action Items view
   Then I can see the Action Items title 'My Action Items'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Action Items form
  Go To  ${PLONE_URL}/++add++Action Items

a Action Items 'My Action Items'
  Create content  type=Action Items  id=my-action_items  title=My Action Items

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Action Items view
  Go To  ${PLONE_URL}/my-action_items
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Action Items with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Action Items title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
