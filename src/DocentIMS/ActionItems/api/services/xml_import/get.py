    # -*- coding: utf-8 -*-
    from plone import api
    from plone.restapi.services import Service
    from Products.CMFCore.utils import getToolByName
    from Products.CMFCore.exportimport.catalog import importCatalogTool
    from Products.GenericSetup.context import SnapshotImportContext
    from io import BytesIO

    # from plone.protect.interfaces import IDisableCSRFProtection
    # from zope.interface import alsoProvides


    class XmlImport(Service):
        def reply(self):
            # alsoProvides(self.request, IDisableCSRFProtection)
            xml_data = b"""\
                <?xml version="1.0"?>
                <object name="portal_catalog" meta_type="Plone Catalog Tool">
                <index name="my_index" meta_type="FieldIndex" />
                </object>
            """

            portal = api.portal.get()
            setup = getToolByName(portal, "portal_setup")

            # Create a fake import context that returns our XML
            class InlineImportContext(SnapshotImportContext):
                def readDataFile(self, filename):
                    if filename == "catalog.xml":
                        return xml_data
                    return None

            context = InlineImportContext(setup, "utf-8")
            importCatalogTool(context)  # now only one argument

            self.request.response.setStatus(200)
            return {
                "status": "success",
                "message": "Catalog XML imported from inline data."
            }
