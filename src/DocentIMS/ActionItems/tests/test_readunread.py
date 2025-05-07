# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_FUNCTIONAL_TESTING
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletType
from zope.component import getUtility

import unittest


class PortletIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_readunread_is_registered(self):
        portlet = getUtility(
            IPortletType,
            name='DocentIMS.ActionItems.portlets.Readunread',
        )
        self.assertEqual(portlet.addview, 'DocentIMS.ActionItems.portlets.Readunread')


class PortletFunctionalTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
