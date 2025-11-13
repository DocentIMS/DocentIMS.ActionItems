# -*- coding: utf-8 -*-
"""Tests for item_count API service."""
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from DateTime import DateTime

import unittest


class ItemCountServiceIntegrationTest(unittest.TestCase):
    """Test the @item_count REST API service."""

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Set up test fixtures."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        # Get current user
        self.current_user = api.user.get_current()
        self.user_id = self.current_user.getId()
        self.user_email = self.current_user.getProperty('email')

        # Set user property for timezone
        self.current_user.setMemberProperties(mapping={'timezone': 'UTC'})

        # Create test content
        self._create_test_content()

    def _create_test_content(self):
        """Create test action items and meetings."""
        # Create action items
        try:
            self.action_item1 = api.content.create(
                container=self.portal,
                type='action_items',
                title='Test Action Item 1',
                assigned_id=self.user_id,
            )
            api.content.transition(obj=self.action_item1, transition='publish')
        except Exception:
            # Content type might not be fully set up
            pass

        # Create meetings
        try:
            self.meeting1 = api.content.create(
                container=self.portal,
                type='meeting',
                title='Test Meeting 1',
                attendees=[self.user_id],
                start=DateTime(),
            )
        except Exception:
            # Content type might not be fully set up
            pass

    def test_service_endpoint_exists(self):
        """Test that the @item_count endpoint exists."""
        response = self.portal.restrictedTraverse('@@item_count')
        self.assertTrue(response is not None)

    def test_item_count_not_expanded(self):
        """Test item_count response when not expanded."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        service = ItemCount(self.portal, self.request)
        result = service(expand=False)

        self.assertIn('item_count', result)
        self.assertIn('@id', result['item_count'])
        self.assertIn('/@item_count', result['item_count']['@id'])

    def test_item_count_with_user(self):
        """Test item_count with authenticated user."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        # Set user in request
        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        self.assertIn('item_count', result)
        item_count = result['item_count']
        self.assertIn('dashboard-list', item_count)

    def test_item_count_dashboard_structure(self):
        """Test the structure of dashboard-list data."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        # Check expected fields
        expected_fields = [
            'site_url',
            'meetings',
            'meeting_list',
            'last_updated',
            'last_login_time',
            'ais',
            'your_team_role',
            'notification_list',
            'urgency_list',
            'project_color',
            'mark_color',
            'short_name',
            'portlet_content',
            'user',
        ]

        for field in expected_fields:
            self.assertIn(field, dashboard, f"Field '{field}' should be in dashboard-list")

    def test_item_count_meeting_counts(self):
        """Test that meeting counts are calculated correctly."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        # Check meeting data
        self.assertIn('meetings', dashboard)
        self.assertIsInstance(dashboard['meetings'], int)
        self.assertGreaterEqual(dashboard['meetings'], 0)

        # Check meeting list structure
        self.assertIn('meeting_list', dashboard)
        self.assertIsInstance(dashboard['meeting_list'], list)

    def test_item_count_action_items_count(self):
        """Test that action items count is calculated."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        self.assertIn('ais', dashboard)
        self.assertIsInstance(dashboard['ais'], int)
        self.assertGreaterEqual(dashboard['ais'], 0)

    def test_item_count_urgency_list(self):
        """Test that urgency list is properly structured."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']
        urgency_list = dashboard['urgency_list']

        self.assertIsInstance(urgency_list, list)

        # Should have urgency categories
        for urgency_item in urgency_list:
            self.assertIn('name', urgency_item)
            self.assertIn('count', urgency_item)
            self.assertIsInstance(urgency_item['count'], int)

    def test_item_count_notification_list(self):
        """Test that notification list is properly structured."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']
        notification_list = dashboard['notification_list']

        self.assertIsInstance(notification_list, list)

        # Each notification type should have name and count
        for notification in notification_list:
            self.assertIn('name', notification)
            self.assertIn('count', notification)
            self.assertIsInstance(notification['count'], int)

    def test_item_count_user_information(self):
        """Test that user information is included."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        # Should include user fullname
        self.assertIn('user', dashboard)
        self.assertIsNotNone(dashboard['user'])

        # Should include team role
        self.assertIn('your_team_role', dashboard)

    def test_item_count_last_updated(self):
        """Test that last_updated field is formatted correctly."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']
        last_updated = dashboard['last_updated']

        # Should be a formatted date string
        self.assertIsInstance(last_updated, str)
        self.assertNotEqual(last_updated, '')

    def test_item_count_portlet_content(self):
        """Test that portlet content (news items) is included."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        # Create a news item
        api.content.create(
            container=self.portal,
            type='News Item',
            title='Test News',
            description='Test news description',
        )

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']
        portlet_content = dashboard['portlet_content']

        self.assertIsInstance(portlet_content, list)

        if portlet_content:
            news_item = portlet_content[0]
            self.assertIn('title', news_item)
            self.assertIn('description', news_item)
            self.assertIn('url', news_item)

    def test_item_count_site_url(self):
        """Test that site_url is included."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        self.assertIn('site_url', dashboard)
        self.assertEqual(dashboard['site_url'], self.portal.absolute_url())

    def test_item_count_without_user(self):
        """Test item_count when no user is provided."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        # Don't set user in request
        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        item_count = result['item_count']
        dashboard = item_count.get('dashboard-list')

        # Should return None when no user
        self.assertIsNone(dashboard)

    def test_item_count_ip_address_check(self):
        """Test that IP address is extracted correctly."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        # Set IP address headers
        self.request.environ['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        # Should execute successfully
        self.assertIn('item_count', result)
        self.assertIn('dashboard-list', result['item_count'])

    def test_item_count_last_login_time_check(self):
        """Test that last_login_time is evaluated correctly."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        # Should have last_login_time boolean check
        self.assertIn('last_login_time', dashboard)
        self.assertIsInstance(dashboard['last_login_time'], bool)

    def test_item_count_project_colors(self):
        """Test that project colors are included."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        self.assertIn('project_color', dashboard)
        self.assertIn('mark_color', dashboard)

    def test_item_count_short_name(self):
        """Test that project short name is included."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = self.user_id

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        dashboard = result['item_count']['dashboard-list']

        self.assertIn('short_name', dashboard)

    def test_item_count_with_nonexistent_user(self):
        """Test item_count with nonexistent user."""
        from DocentIMS.ActionItems.api.services.item_count.get import ItemCount

        self.request.user = 'nonexistent_user_12345'

        service = ItemCount(self.portal, self.request)
        result = service(expand=True)

        # Should handle gracefully
        self.assertIn('item_count', result)
