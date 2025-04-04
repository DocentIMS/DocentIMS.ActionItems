# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.behaviors.auto_publish_beahvior import IAutoPublishBeahviorMarker
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class AutoPublishBeahviorIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_auto_publish_beahvior(self):
        behavior = getUtility(IBehavior, 'DocentIMS.ActionItems.auto_publish_beahvior')
        self.assertEqual(
            behavior.marker,
            IAutoPublishBeahviorMarker,
        )
