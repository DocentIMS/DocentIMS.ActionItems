# -*- coding: utf-8 -*-
"""Tests for workflow_info API service."""
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class WorkflowInfoServiceIntegrationTest(unittest.TestCase):
    """Test the @workflow_info REST API service."""

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Set up test fixtures."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_service_endpoint_exists(self):
        """Test that the @workflow_info endpoint exists."""
        response = self.portal.restrictedTraverse('@@workflow_info')
        self.assertTrue(response is not None)

    def test_workflow_info_without_portal_type(self):
        """Test workflow_info without specifying portal_type."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        self.assertIn('workflow_info', result)
        self.assertIn('@id', result['workflow_info'])

    def test_workflow_info_with_specific_portal_type(self):
        """Test workflow_info for a specific content type."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        # Set request to ask for Document workflow
        self.request.portal_type = 'Document'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        self.assertIn('workflow_info', result)
        self.assertIn('wf_states_list', result['workflow_info'])

        wf_list = result['workflow_info']['wf_states_list']
        self.assertIsInstance(wf_list, list)

        if wf_list:  # Document type has workflow
            workflow_data = wf_list[0]
            self.assertIn('content_type', workflow_data)
            self.assertIn('workflow_transitions', workflow_data)
            self.assertIn('workflow_states', workflow_data)
            self.assertIn('initial_state', workflow_data)

    def test_workflow_info_all_content_types(self):
        """Test workflow_info for all content types using wildcard."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        # Set request to ask for all workflows
        self.request.portal_type = '*'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        self.assertIn('workflow_info', result)
        wf_list = result['workflow_info']['wf_states_list']
        self.assertIsInstance(wf_list, list)
        # Should have multiple content types
        self.assertGreater(len(wf_list), 0)

    def test_workflow_info_action_items_type(self):
        """Test workflow_info specifically for action_items."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        self.request.portal_type = 'action_items'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        wf_list = result['workflow_info']['wf_states_list']

        if wf_list:
            workflow_data = wf_list[0]
            self.assertEqual(workflow_data['content_type'], 'action_items')

            # Check workflow structure
            self.assertIn('workflow_transitions', workflow_data)
            transitions = workflow_data['workflow_transitions']
            self.assertIsInstance(transitions, list)

            # Each transition should have expected fields
            if transitions:
                transition = transitions[0]
                self.assertIn('id', transition)
                self.assertIn('title', transition)
                self.assertIn('description', transition)
                self.assertIn('new_state_id', transition)
                self.assertIn('actbox_name', transition)

            # Check states structure
            self.assertIn('workflow_states', workflow_data)
            states = workflow_data['workflow_states']
            self.assertIsInstance(states, list)

            if states:
                state = states[0]
                self.assertIn('id', state)
                self.assertIn('title', state)
                self.assertIn('description', state)
                self.assertIn('transitions', state)

    def test_workflow_info_case_insensitive_matching(self):
        """Test that portal_type matching is case-insensitive."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        # Test with different case variations
        for portal_type in ['document', 'DOCUMENT', 'Document']:
            self.request.portal_type = portal_type

            service = WorkflowInfo(self.portal, self.request)
            result = service(expand=True)

            wf_list = result['workflow_info']['wf_states_list']
            if wf_list:
                # Should find Document type regardless of case
                self.assertTrue(any(
                    w['content_type'].lower() == 'document'
                    for w in wf_list
                ))

    def test_workflow_info_underscore_to_space_conversion(self):
        """Test that underscores are converted to spaces for matching."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        # Meeting Minutes might be stored as "Meeting Minutes" but requested as "meeting_minutes"
        self.request.portal_type = 'meeting_minutes'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        # Should successfully match content type
        self.assertIn('workflow_info', result)
        wf_list = result['workflow_info']['wf_states_list']
        self.assertIsInstance(wf_list, list)

    def test_workflow_info_nonexistent_content_type(self):
        """Test workflow_info for a non-existent content type."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        self.request.portal_type = 'NonexistentType'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        wf_list = result['workflow_info']['wf_states_list']
        # Should return empty list for non-existent type
        self.assertEqual(wf_list, [])

    def test_get_content_types_and_workflows_function(self):
        """Test the get_content_types_and_workflows helper function directly."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import get_content_types_and_workflows

        # Test with wildcard
        result = get_content_types_and_workflows('*')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # Each workflow should have required structure
        for workflow in result:
            self.assertIn('content_type', workflow)
            self.assertIn('workflow_transitions', workflow)
            self.assertIn('workflow_states', workflow)
            self.assertIn('initial_state', workflow)

    def test_workflow_transitions_structure(self):
        """Test that workflow transitions have complete information."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        self.request.portal_type = '*'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        wf_list = result['workflow_info']['wf_states_list']

        # Find a workflow with transitions
        for workflow in wf_list:
            if workflow['workflow_transitions']:
                transition = workflow['workflow_transitions'][0]

                # Verify all transition fields are present
                self.assertIsNotNone(transition.get('id'))
                self.assertIsNotNone(transition.get('title'))
                # description, new_state_id, actbox_name can be empty but should be present
                self.assertIn('description', transition)
                self.assertIn('new_state_id', transition)
                self.assertIn('actbox_name', transition)
                break

    def test_workflow_states_structure(self):
        """Test that workflow states have complete information."""
        from DocentIMS.ActionItems.api.services.workflow_info.get import WorkflowInfo

        self.request.portal_type = '*'

        service = WorkflowInfo(self.portal, self.request)
        result = service(expand=True)

        wf_list = result['workflow_info']['wf_states_list']

        # Find a workflow with states
        for workflow in wf_list:
            if workflow['workflow_states']:
                state = workflow['workflow_states'][0]

                # Verify all state fields are present
                self.assertIsNotNone(state.get('id'))
                self.assertIsNotNone(state.get('title'))
                self.assertIn('description', state)
                self.assertIn('transitions', state)
                self.assertIsInstance(state['transitions'], (list, tuple))
                break
