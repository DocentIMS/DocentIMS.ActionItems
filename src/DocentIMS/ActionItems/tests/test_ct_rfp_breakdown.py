# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class RfpBreakdownIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_rfp_breakdown_schema(self):
        fti = queryUtility(IDexterityFTI, name='rfp_breakdown')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('rfp_breakdown')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_rfp_breakdown_fti(self):
        fti = queryUtility(IDexterityFTI, name='rfp_breakdown')
        self.assertTrue(fti)

    def test_ct_rfp_breakdown_factory(self):
        fti = queryUtility(IDexterityFTI, name='rfp_breakdown')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_rfp_breakdown_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='rfp_breakdown',
            id='rfp_breakdown',
        )


        parent = obj.__parent__
        self.assertIn('rfp_breakdown', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('rfp_breakdown', parent.objectIds())

    def test_ct_rfp_breakdown_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='rfp_breakdown')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
