# -*- coding: utf-8 -*-
from io import BytesIO
from docx import Document

def handler(obj, event):
    """ Event handler
    """
    ## updates word properties (where the file came from)
    file_field = getattr(obj, "file", None)
    # check if file is word
    
    if file_field and getattr(file_field, "contentType", None) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' :
            # if file_field.contentType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            file_data = file_field.data
            filename = getattr(file_field, "filename", obj.getId()) or "attachment"
            try:
                doc = Document(BytesIO(file_data))
                props = doc.core_properties
                props.subject = obj.absolute_url()
                # props.came_from = obj.absolute_url()
                buffer = BytesIO()
                doc.save(buffer)
                obj.file.data = buffer.getvalue()
                
            
            except Exception as e:
                    pass
                    
