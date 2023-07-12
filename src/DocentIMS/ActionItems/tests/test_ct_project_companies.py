# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.content.project_companies import IProjectCompanies  # NOQA E501
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class ProjectCompaniesIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_project_companies_schema(self):
        fti = queryUtility(IDexterityFTI, name='project_companies')
        schema = fti.lookupSchema()
        self.assertEqual(IProjectCompanies, schema)

    def test_ct_project_companies_fti(self):
        fti = queryUtility(IDexterityFTI, name='project_companies')
        self.assertTrue(fti)

    def test_ct_project_companies_factory(self):
        fti = queryUtility(IDexterityFTI, name='project_companies')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IProjectCompanies.providedBy(obj),
            u'IProjectCompanies not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_project_companies_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='project_companies',
            id='project_companies',
        )

        self.assertTrue(
            IProjectCompanies.providedBy(obj),
            u'IProjectCompanies not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('project_companies', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('project_companies', parent.objectIds())

    def test_ct_project_companies_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='project_companies')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
