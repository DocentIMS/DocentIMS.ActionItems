# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_feedback.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_feedback.robot
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

Scenario: As a site administrator I can add a Feedback
  Given a logged-in site administrator
    and an add Feedback form
   When I type 'My Feedback' into the title field
    and I submit the form
   Then a Feedback with the title 'My Feedback' has been created

Scenario: As a site administrator I can view a Feedback
  Given a logged-in site administrator
    and a Feedback 'My Feedback'
   When I go to the Feedback view
   Then I can see the Feedback title 'My Feedback'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Feedback form
  Go To  ${PLONE_URL}/++add++Feedback

a Feedback 'My Feedback'
  Create content  type=Feedback  id=my-feedback  title=My Feedback

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Feedback view
  Go To  ${PLONE_URL}/my-feedback
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Feedback with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Feedback title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
