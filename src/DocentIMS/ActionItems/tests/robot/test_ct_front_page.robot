# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_front_page.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_front_page.robot
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

Scenario: As a site administrator I can add a FrontPage
  Given a logged-in site administrator
    and an add FrontPage form
   When I type 'My FrontPage' into the title field
    and I submit the form
   Then a FrontPage with the title 'My FrontPage' has been created

Scenario: As a site administrator I can view a FrontPage
  Given a logged-in site administrator
    and a FrontPage 'My FrontPage'
   When I go to the FrontPage view
   Then I can see the FrontPage title 'My FrontPage'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add FrontPage form
  Go To  ${PLONE_URL}/++add++FrontPage

a FrontPage 'My FrontPage'
  Create content  type=FrontPage  id=my-front_page  title=My FrontPage

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the FrontPage view
  Go To  ${PLONE_URL}/my-front_page
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a FrontPage with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the FrontPage title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
