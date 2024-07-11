# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.behaviors.only_office_file import IOnlyOfficeFileMarker
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class OnlyOfficeFileIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_only_office_file(self):
        behavior = getUtility(IBehavior, 'DocentIMS.ActionItems.only_office_file')
        self.assertEqual(
            behavior.marker,
            IOnlyOfficeFileMarker,
        )
