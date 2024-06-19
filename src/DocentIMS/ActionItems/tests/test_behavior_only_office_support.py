# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.behaviors.only_office_support import IOnlyOfficeSupportMarker
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class OnlyOfficeSupportIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_only_office_support(self):
        behavior = getUtility(IBehavior, 'DocentIMS.ActionItems.only_office_support')
        self.assertEqual(
            behavior.marker,
            IOnlyOfficeSupportMarker,
        )
