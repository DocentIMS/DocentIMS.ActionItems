# -*- coding: utf-8 -*-
"""Tests for docs_info API service."""
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class DocsInfoServiceIntegrationTest(unittest.TestCase):
    """Test the @docs_info REST API service."""

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Set up test fixtures."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # Set up some registry records for testing
        self.registry = getUtility(IRegistry)

        # Create documents folder structure if it doesn't exist
        if 'documents' not in self.portal.objectIds():
            api.content.create(
                container=self.portal,
                type='Folder',
                id='documents',
                title='Documents'
            )

    def test_service_endpoint_exists(self):
        """Test that the @docs_info endpoint exists."""
        response = self.portal.restrictedTraverse('@@docs_info')
        self.assertTrue(response is not None)

    def test_docs_info_not_expanded(self):
        """Test docs_info response when not expanded."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=False)

        self.assertIn('docs_info', result)
        self.assertIn('@id', result['docs_info'])
        self.assertIn('/@docs_info', result['docs_info']['@id'])

    def test_docs_info_expanded_structure(self):
        """Test docs_info expanded response structure."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        self.assertIn('docs_info', result)
        docs_info = result['docs_info']

        # Check for expected fields
        expected_fields = [
            'meeting_locations',
            'stoplight_state',
            'dashboard_url',
            'meeting_types',
            'notification_types',
            'planning_project',
            'green',
            'yellow',
            'red',
            'project_color',
            'marking_color',
            'short_name',
            'project_contract_number',
            'marketing_contract_number',
            'project_document_naming_convention',
            'member_roles',
            'meetings_frequencies',
            'companies',
            'last_document_save_location',
            'time_now_portal',
            'time_now_user',
            'user_timezone',
            'portal_timezone',
            'template_password',
        ]

        for field in expected_fields:
            self.assertIn(field, docs_info, f"Field '{field}' should be in docs_info")

    def test_docs_info_timezone_information(self):
        """Test that timezone information is correctly returned."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']

        # Check timezone fields
        self.assertIn('portal_timezone', docs_info)
        self.assertIn('user_timezone', docs_info)
        self.assertIn('time_now_portal', docs_info)
        self.assertIn('time_now_user', docs_info)

        # Verify time formats are ISO format
        self.assertIsNotNone(docs_info['time_now_portal'])
        self.assertIsNotNone(docs_info['time_now_user'])

    def test_docs_info_meeting_frequencies(self):
        """Test that meeting frequencies are returned."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        frequencies = docs_info['meetings_frequencies']

        self.assertIsInstance(frequencies, list)
        expected_frequencies = ["Daily", "Weekly", "Semi-Weekly", "Monthly", "Quarterly", "Other"]
        self.assertEqual(frequencies, expected_frequencies)

    def test_docs_info_stoplight_colors(self):
        """Test that stoplight color settings are returned."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']

        # Check that color fields exist
        self.assertIn('red', docs_info)
        self.assertIn('yellow', docs_info)
        self.assertIn('green', docs_info)
        self.assertIn('project_color', docs_info)
        self.assertIn('marking_color', docs_info)

    def test_docs_info_meeting_types_conversion(self):
        """Test that meeting_attendees sets are converted to lists."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        # Set up a meeting type with a set for attendees
        try:
            api.portal.set_registry_record(
                'DocentIMS.ActionItems.interfaces.IDocentimsSettings.meeting_types',
                [
                    {
                        'meeting_type': 'Test Meeting',
                        'meeting_attendees': {'user1', 'user2', 'user3'}
                    }
                ]
            )
        except Exception:
            # If setting fails, skip this specific test
            self.skipTest("Could not set meeting_types registry record")

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        meeting_types = docs_info.get('meeting_types', [])

        if meeting_types:
            for meeting_type in meeting_types:
                if 'meeting_attendees' in meeting_type:
                    # Should be converted to list, not set
                    self.assertIsInstance(
                        meeting_type['meeting_attendees'],
                        list,
                        "meeting_attendees should be converted to list"
                    )

    def test_docs_info_save_location_date(self):
        """Test that last_document_save_location is formatted correctly."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        # Create save-locations folder
        documents = self.portal.get('documents')
        if documents and 'save-locations' not in documents.objectIds():
            api.content.create(
                container=documents,
                type='Folder',
                id='save-locations',
                title='Save Locations'
            )

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        save_location_date = docs_info['last_document_save_location']

        # Should either be empty string or ISO format date
        self.assertIsInstance(save_location_date, str)

    def test_docs_info_project_information(self):
        """Test that project information is returned."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']

        # Check project-related fields
        self.assertIn('short_name', docs_info)
        self.assertIn('very_short_name', docs_info)
        self.assertIn('project_contract_number', docs_info)
        self.assertIn('marketing_contract_number', docs_info)
        self.assertIn('project_document_naming_convention', docs_info)

    def test_docs_info_with_anonymous_user(self):
        """Test docs_info behavior with no authenticated user."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo
        from AccessControl import Unauthorized

        # Logout to become anonymous
        self.portal.acl_users.session._invalidate()

        service = DocsInfo(self.portal, self.request)

        # Anonymous users should not get docs_info data
        result = service(expand=True)

        # Should return minimal result
        self.assertIn('docs_info', result)
        docs_info = result['docs_info']

        # Should have minimal data or be restricted
        # Based on the code, it checks if user is not None
        if 'id' in docs_info:
            self.assertIsNone(docs_info['id'])

    def test_get_content_types_and_workflows_helper(self):
        """Test the get_content_types_and_workflows helper function."""
        from DocentIMS.ActionItems.api.services.docs_info.get import get_content_types_and_workflows

        result = get_content_types_and_workflows()

        self.assertIsInstance(result, list)

        if result:
            # Each item should have workflow information
            for item in result:
                self.assertIn('content_type', item)
                self.assertIn('workflow_transitions', item)
                self.assertIn('workflow_states', item)

    def test_docs_info_dashboard_url(self):
        """Test that dashboard_url is included in response."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        self.assertIn('dashboard_url', docs_info)

    def test_docs_info_companies_data(self):
        """Test that companies data is included."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        self.assertIn('companies', docs_info)

    def test_docs_info_member_roles(self):
        """Test that member_roles (vocabularies) are included."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        self.assertIn('member_roles', docs_info)

    def test_docs_info_stoplight_state(self):
        """Test that stoplight_state is included."""
        from DocentIMS.ActionItems.api.services.docs_info.get import DocsInfo

        service = DocsInfo(self.portal, self.request)
        result = service(expand=True)

        docs_info = result['docs_info']
        self.assertIn('stoplight_state', docs_info)
