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


class ActionItemsIntegrationTest(unittest.TestCase):

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_action_items_schema(self):
        fti = queryUtility(IDexterityFTI, name='Action Items')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Action Items')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_action_items_fti(self):
        fti = queryUtility(IDexterityFTI, name='Action Items')
        self.assertTrue(fti)

    def test_ct_action_items_factory(self):
        fti = queryUtility(IDexterityFTI, name='Action Items')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_action_items_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Action Items',
            id='action_items',
        )


        parent = obj.__parent__
        self.assertIn('action_items', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('action_items', parent.objectIds())

    def test_ct_action_items_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Action Items')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_action_items_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Action Items')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'action_items_id',
            title='Action Items container',
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
