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


class NotesIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_notes_schema(self):
        fti = queryUtility(IDexterityFTI, name='Notes')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Notes')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_notes_fti(self):
        fti = queryUtility(IDexterityFTI, name='Notes')
        self.assertTrue(fti)

    def test_ct_notes_factory(self):
        fti = queryUtility(IDexterityFTI, name='Notes')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_notes_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Notes',
            id='notes',
        )


        parent = obj.__parent__
        self.assertIn('notes', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('notes', parent.objectIds())

    def test_ct_notes_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Notes')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
