# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.content.sow_analysis import ISowAnalysis  # NOQA E501
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class SowAnalysisIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_sow_analysis_schema(self):
        fti = queryUtility(IDexterityFTI, name='Sow Analysis')
        schema = fti.lookupSchema()
        self.assertEqual(ISowAnalysis, schema)

    def test_ct_sow_analysis_fti(self):
        fti = queryUtility(IDexterityFTI, name='Sow Analysis')
        self.assertTrue(fti)

    def test_ct_sow_analysis_factory(self):
        fti = queryUtility(IDexterityFTI, name='Sow Analysis')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ISowAnalysis.providedBy(obj),
            u'ISowAnalysis not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_sow_analysis_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Sow Analysis',
            id='sow_analysis',
        )

        self.assertTrue(
            ISowAnalysis.providedBy(obj),
            u'ISowAnalysis not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('sow_analysis', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('sow_analysis', parent.objectIds())

    def test_ct_sow_analysis_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Sow Analysis')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
