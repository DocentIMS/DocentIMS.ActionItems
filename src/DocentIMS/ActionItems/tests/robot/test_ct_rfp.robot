# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_rfp.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_rfp.robot
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

Scenario: As a site administrator I can add a rfp
  Given a logged-in site administrator
    and an add rfp form
   When I type 'My rfp' into the title field
    and I submit the form
   Then a rfp with the title 'My rfp' has been created

Scenario: As a site administrator I can view a rfp
  Given a logged-in site administrator
    and a rfp 'My rfp'
   When I go to the rfp view
   Then I can see the rfp title 'My rfp'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add rfp form
  Go To  ${PLONE_URL}/++add++rfp

a rfp 'My rfp'
  Create content  type=rfp  id=my-rfp  title=My rfp

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the rfp view
  Go To  ${PLONE_URL}/my-rfp
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a rfp with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the rfp title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
