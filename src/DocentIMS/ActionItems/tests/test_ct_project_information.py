# -*- coding: utf-8 -*-
from DocentIMS.ActionItems.content.project_information import IProjectInformation  # NOQA E501
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class ProjectInformationIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_project_information_schema(self):
        fti = queryUtility(IDexterityFTI, name='project_information')
        schema = fti.lookupSchema()
        self.assertEqual(IProjectInformation, schema)

    def test_ct_project_information_fti(self):
        fti = queryUtility(IDexterityFTI, name='project_information')
        self.assertTrue(fti)

    def test_ct_project_information_factory(self):
        fti = queryUtility(IDexterityFTI, name='project_information')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IProjectInformation.providedBy(obj),
            u'IProjectInformation not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_project_information_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='project_information',
            id='project_information',
        )

        self.assertTrue(
            IProjectInformation.providedBy(obj),
            u'IProjectInformation not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('project_information', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('project_information', parent.objectIds())

    def test_ct_project_information_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='project_information')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_project_information_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='project_information')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'project_information_id',
            title='project_information container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
