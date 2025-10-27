# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# -*- coding: utf-8 -*-# import docx
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from io import BytesIO
from plone.app.querystring import queryparser
from Products.CMFCore.utils import getToolByName


from plone.dexterity.utils import iterSchemata
from zope.schema import getFieldsInOrder



from plone import api
from DocentIMS.ActionItems.interfaces import IDocentimsSettings


class IMakeWordDocView(Interface):
    """ Marker Interface for IMakeWordDocView"""

class MakeWordDocView(BrowserView):
    
    def __call__(self):
        context = self.context;selected_file_id = self.request.form.get('selected_file', None)
        
        # Fetch the list of docx files from the templates folder
        # files = self.find_docx_in_templates()
        
        # If no file is found or user hasn't selected one, render a form to choose a file
        if not selected_file:
            return self.index()

        # Check if a file has been selected in the request (from a form submission)
        
        if selected_file_id:
            selected_file = next((f for f in files if f['object'].id == selected_file_id), None)
        else:
            # Default to the first file if nothing is selected
            selected_file = files[0]

        if selected_file:
            # Extract the selected file's data
            file_data = selected_file['object'].file.data
            
            # Wrap in BytesIO for docxtpl
            file_stream = BytesIO(file_data)
            doc = DocxTemplate(file_stream)

            # Get context data for replacements
            replacements = self.get_replacements(context)
            doc.render(replacements)

            # Prepare the output file stream for download
            output_stream = BytesIO()
            doc.save(output_stream)
            output_stream.seek(0)

            # Return the generated document as a downloadable response
            self.request.response.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            self.request.response.setHeader('Content-Disposition', 'attachment; filename="generated.docx"')

            return output_stream.getvalue()

        return "No valid file selected."
    
    def get_replacements(self, context):
        """Get the replacements for the Word template."""
        replacements = {}
        
        for schema in iterSchemata(context):
            schema_obj = schema(context)  # This adapts context to the schema
            for name, field in getFieldsInOrder(schema):
                value = getattr(schema_obj, name, None)
                replacements[name] = value
        
        replacements['title'] = context.Title()
        replacements['description'] = context.Description()
        
        return replacements
    
        
    def find_docx_in_templates(self):
        # Define the path to search within (e.g., /templates)
        folder_path = 'Plone11/templates'
        
        # Search for all File content items within the folder
        documents = api.content.find(portal_type='File', path={'query': folder_path, 'depth': 1})
        
        # Collect the items
        docx_items = []
        for document in documents: 
            obj = document.getObject()
            file_type = obj.file.contentType
            if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                docx_items.append({
                    'title': obj.Title(),
                    'url': obj.absolute_url, 'object': obj,
                    'file_name': obj.file.filename  # Include the filename as well for easier reference
                })
        
        # import pdb; pdb.set_trace()
        return docx_items