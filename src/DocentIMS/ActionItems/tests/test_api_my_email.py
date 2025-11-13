# -*- coding: utf-8 -*-
"""Tests for my_email API service."""
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME

import unittest


class MyEmailServiceIntegrationTest(unittest.TestCase):
    """Test the @my_email REST API service."""

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Set up test fixtures."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # Create test users with different properties
        api.user.create(
            email='testuser1@example.com',
            username='testuser1',
            properties={
                'fullname': 'Test User One',
                'first_name': 'Test',
                'your_team_role': 'Developer',
                'office_phone_number': '555-0001',
                'cellphone_number': '555-0101',
                'company': 'Test Company A',
            }
        )

        api.user.create(
            email='testuser2@example.com',
            username='testuser2',
            properties={
                'fullname': 'Test User Two',
                'first_name': 'Test',
                'your_team_role': 'Manager',
                'office_phone_number': '555-0002',
                'cellphone_number': '555-0102',
                'company': 'Test Company B',
            }
        )

        # Create test group
        api.group.create(
            groupname='test_team',
            title='Test Team',
        )
        api.group.add_user(groupname='test_team', username='testuser1')
        api.group.add_user(groupname='test_team', username='testuser2')

    def test_service_endpoint_exists(self):
        """Test that the @my_email endpoint exists."""
        response = self.portal.restrictedTraverse('@@my_email')
        self.assertTrue(response is not None)

    def test_my_email_current_user(self):
        """Test getting current user's email information."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        service = MyEmail(self.portal, self.request)
        result = service(expand=True)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # Check user data structure
        user_data = result[0]
        self.assertIn('id', user_data)
        self.assertIn('email', user_data)
        self.assertIn('fullname', user_data)
        self.assertIn('roles', user_data)

    def test_my_email_specific_user(self):
        """Test getting specific user's email information."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        # Set request parameter to get specific user
        self.request.set('email', 'testuser1')

        service = MyEmail(self.portal, self.request)
        result = service(expand=True)

        self.assertIsInstance(result, list)
        # First item should be user data, last should be groups
        user_data = result[0]
        self.assertEqual(user_data['fullname'], 'Test User One')
        self.assertEqual(user_data['email'], 'testuser1@example.com')
        self.assertEqual(user_data['your_team_role'], 'Developer')
        self.assertEqual(user_data['company'], 'Test Company A')

    def test_my_email_all_users(self):
        """Test getting all users with wildcard."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        # Set request parameter to get all users
        self.request.set('email', '*')

        service = MyEmail(self.portal, self.request)
        result = service(expand=True)

        self.assertIsInstance(result, list)
        # Should have multiple users plus groups entry
        self.assertGreaterEqual(len(result), 3)  # At least 3: test users + current user + groups

        # Last item should be groups
        groups_data = result[-1]
        self.assertIn('groups', groups_data)

    def test_my_email_includes_group_info(self):
        """Test that group information is included when requesting all users."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        # Add current user to test group
        current = api.user.get_current()
        api.group.add_user(groupname='test_team', user=current)

        self.request.set('email', '*')

        service = MyEmail(self.portal, self.request)
        result = service(expand=True)

        # Last item should contain groups
        groups_data = result[-1]
        self.assertIn('groups', groups_data)
        self.assertIsInstance(groups_data['groups'], list)

        # Find our test group
        test_group = None
        for group in groups_data['groups']:
            if group['id'] == 'test_team':
                test_group = group
                break

        self.assertIsNotNone(test_group)
        self.assertEqual(test_group['title'], 'Test Team')
        self.assertIn('groupMembers', test_group)
        self.assertGreaterEqual(len(test_group['groupMembers']), 2)

    def test_my_email_user_properties(self):
        """Test that all expected user properties are returned."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        self.request.set('email', 'testuser2')

        service = MyEmail(self.portal, self.request)
        result = service(expand=True)

        user_data = result[0]

        # Check all expected properties
        expected_props = [
            'id', 'email', 'fullname', 'roles', 'last_name',
            'first_name', 'your_team_role', 'office_phone_number',
            'cellphone_number', 'company'
        ]

        for prop in expected_props:
            self.assertIn(prop, user_data, f"Property '{prop}' missing from user data")

    def test_my_email_not_expanded(self):
        """Test service response when not expanded."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        service = MyEmail(self.portal, self.request)
        result = service(expand=False)

        self.assertIn('my_email', result)
        self.assertIn('@id', result['my_email'])
        self.assertIn('/@my_email', result['my_email']['@id'])

    def test_my_email_nonexistent_user(self):
        """Test requesting a nonexistent user."""
        from DocentIMS.ActionItems.api.services.my_email.get import MyEmail

        self.request.set('email', 'nonexistent_user')

        service = MyEmail(self.portal, self.request)
        result = service(expand=True)

        # Should return list with groups only, since user doesn't exist
        # The code tries to get user but will fail, need to verify behavior
        self.assertIsInstance(result, list)
