# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s DocentIMS.ActionItems -t test_docent_misc_document.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src DocentIMS.ActionItems.testing.DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/DocentIMS/ActionItems/tests/robot/test_docent_misc_document.robot
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

Scenario: As a site administrator I can add a docent_misc_document
  Given a logged-in site administrator
    and an add docent_misc_document form
   When I type 'My docent_misc_document' into the title field
    and I submit the form
   Then a docent_misc_document with the title 'My docent_misc_document' has been created

Scenario: As a site administrator I can view a docent_misc_document
  Given a logged-in site administrator
    and a docent_misc_document 'My docent_misc_document'
   When I go to the docent_misc_document view
   Then I can see the docent_misc_document title 'My docent_misc_document'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add docent_misc_document form
  Go To  ${PLONE_URL}/++add++docent_misc_document

a docent_misc_document 'My docent_misc_document'
  Create content  type=docent_misc_document  id=my-docent_misc_document  title=My docent_misc_document

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the docent_misc_document view
  Go To  ${PLONE_URL}/my-docent_misc_document
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a docent_misc_document with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the docent_misc_document title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
