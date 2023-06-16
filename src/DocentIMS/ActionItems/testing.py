# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import DocentIMS.ActionItems


class DocentimsActionitemsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=DocentIMS.ActionItems)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'DocentIMS.ActionItems:default')


DOCENTIMS_ACTIONITEMS_FIXTURE = DocentimsActionitemsLayer()


DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DOCENTIMS_ACTIONITEMS_FIXTURE,),
    name='DocentimsActionitemsLayer:IntegrationTesting',
)


DOCENTIMS_ACTIONITEMS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DOCENTIMS_ACTIONITEMS_FIXTURE,),
    name='DocentimsActionitemsLayer:FunctionalTesting',
)


DOCENTIMS_ACTIONITEMS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DOCENTIMS_ACTIONITEMS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='DocentimsActionitemsLayer:AcceptanceTesting',
)
