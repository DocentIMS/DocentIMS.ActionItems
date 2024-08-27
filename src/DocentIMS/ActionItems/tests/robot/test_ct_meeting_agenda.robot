# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_meeting_agenda.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_meeting_agenda.robot
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

Scenario: As a site administrator I can add a Meeting Agenda
  Given a logged-in site administrator
    and an add Meeting Agenda form
   When I type 'My Meeting Agenda' into the title field
    and I submit the form
   Then a Meeting Agenda with the title 'My Meeting Agenda' has been created

Scenario: As a site administrator I can view a Meeting Agenda
  Given a logged-in site administrator
    and a Meeting Agenda 'My Meeting Agenda'
   When I go to the Meeting Agenda view
   Then I can see the Meeting Agenda title 'My Meeting Agenda'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Meeting Agenda form
  Go To  ${PLONE_URL}/++add++Meeting Agenda

a Meeting Agenda 'My Meeting Agenda'
  Create content  type=Meeting Agenda  id=my-meeting_agenda  title=My Meeting Agenda

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Meeting Agenda view
  Go To  ${PLONE_URL}/my-meeting_agenda
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Meeting Agenda with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Meeting Agenda title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
