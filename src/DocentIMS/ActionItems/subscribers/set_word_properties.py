# -*- coding: utf-8 -*-
from io import BytesIO
from docx import Document

def handler(obj, event):
    """ Event handler
    """
    # print(u"{0} on object {1}".format(event.__class__, obj.absolute_url()))
    # 1 check if file is word
    # 2 if word, change properties
    # save 
    import pdb; pdb.set_trace()
    file_field = getattr(obj, "file", None)
    # check if file is word
    if file_field and not getattr(file_field, "data", None):
        file_data = file_field.data
        filename = getattr(file_field, "filename", obj.getId()) or "attachment"
        if filename.lower().endswith(".docx"):
            try:
                doc = Document(BytesIO(file_data))
                props = doc.core_properties
                props.subject = obj.absolute_url()
                buffer = BytesIO()
                doc.save(buffer)
                file_data = buffer.getvalue()
            except Exception as e:
                pass
                
