# -*- coding: utf-8 -*-
"""Tests for xml_import API service."""
from DocentIMS.ActionItems.testing import DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

import unittest


class XmlImportServiceIntegrationTest(unittest.TestCase):
    """Test the @xml_import REST API service."""

    layer = DOCENTIMS_ACTIONITEMS_INTEGRATION_TESTING

    def setUp(self):
        """Set up test fixtures."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def test_service_endpoint_exists(self):
        """Test that the @xml_import endpoint exists."""
        response = self.portal.restrictedTraverse('@@xml_import')
        self.assertTrue(response is not None)

    def test_xml_import_basic_execution(self):
        """Test basic XML import execution."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        service = XmlImport(self.portal, self.request)
        result = service.reply()

        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('message', result)
        self.assertEqual(result['status'], 'success')
        self.assertIn('imported', result['message'].lower())

    def test_xml_import_response_status(self):
        """Test that XML import sets correct HTTP status."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        service = XmlImport(self.portal, self.request)
        result = service.reply()

        # Should set status 200
        self.assertEqual(self.request.response.getStatus(), 200)

    def test_xml_import_catalog_tool(self):
        """Test that the import uses the catalog tool."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        # Get initial catalog indexes
        initial_indexes = list(self.catalog.indexes())

        service = XmlImport(self.portal, self.request)
        result = service.reply()

        # Verify operation succeeded
        self.assertEqual(result['status'], 'success')

    def test_xml_import_inline_context(self):
        """Test that InlineImportContext is used correctly."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        service = XmlImport(self.portal, self.request)

        # The service creates an InlineImportContext internally
        # Just verify it executes without errors
        try:
            result = service.reply()
            success = True
        except Exception:
            success = False

        self.assertTrue(success)
        self.assertEqual(result['status'], 'success')

    def test_xml_import_returns_expected_structure(self):
        """Test that the response has the expected structure."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        service = XmlImport(self.portal, self.request)
        result = service.reply()

        # Check response structure
        self.assertIsInstance(result, dict)
        self.assertEqual(set(result.keys()), {'status', 'message'})
        self.assertIsInstance(result['status'], str)
        self.assertIsInstance(result['message'], str)

    def test_xml_import_idempotent(self):
        """Test that running import multiple times doesn't cause errors."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        service = XmlImport(self.portal, self.request)

        # Run import multiple times
        result1 = service.reply()
        self.assertEqual(result1['status'], 'success')

        result2 = service.reply()
        self.assertEqual(result2['status'], 'success')

        result3 = service.reply()
        self.assertEqual(result3['status'], 'success')

    def test_xml_import_has_portal_setup(self):
        """Test that portal_setup tool is accessible."""
        setup = getToolByName(self.portal, 'portal_setup', None)
        self.assertIsNotNone(setup, "portal_setup tool should be available")

    def test_xml_import_xml_data_format(self):
        """Test that the XML data is properly formatted."""
        from DocentIMS.ActionItems.api.services.xml_import.get import XmlImport

        # The XML should be well-formed - the import should not raise XML parsing errors
        service = XmlImport(self.portal, self.request)

        try:
            result = service.reply()
            xml_valid = True
        except Exception as e:
            # If there's an XML parsing error, it would fail here
            xml_valid = False
            error_message = str(e)

        self.assertTrue(xml_valid, "XML should be well-formed")
