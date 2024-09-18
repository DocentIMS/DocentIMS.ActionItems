# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_post_it_note.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_post_it_note.robot
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

Scenario: As a site administrator I can add a PostIt Note
  Given a logged-in site administrator
    and an add PostIt Note form
   When I type 'My PostIt Note' into the title field
    and I submit the form
   Then a PostIt Note with the title 'My PostIt Note' has been created

Scenario: As a site administrator I can view a PostIt Note
  Given a logged-in site administrator
    and a PostIt Note 'My PostIt Note'
   When I go to the PostIt Note view
   Then I can see the PostIt Note title 'My PostIt Note'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PostIt Note form
  Go To  ${PLONE_URL}/++add++PostIt Note

a PostIt Note 'My PostIt Note'
  Create content  type=PostIt Note  id=my-post_it_note  title=My PostIt Note

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PostIt Note view
  Go To  ${PLONE_URL}/my-post_it_note
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PostIt Note with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PostIt Note title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
