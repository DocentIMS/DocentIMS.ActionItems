from AccessControl.SecurityManagement import getSecurityManager
from plone.app.users.browser.account import getSchema
from plone.app.users.schema import IUserDataSchema
from plone.base import PloneMessageFactory as _ 
from Products.CMFPlone.utils import get_portal  
from plone.app.users.browser.userdatapanel import UserDataPanel, UserDataPanelAdapter


class CustomUserDataPanel(UserDataPanel):

    def updateFields(self):
        super().updateFields()
        # Get the existing field names in their current order
        existing_field_names = list(self.fields.keys())

        # Move 'last_name/first_name' to the front, keeping all other fields in their original order
        reordered_fields = ['last_name', 'first_name'] + [name for name in existing_field_names if name not in ['first_name', 'last_name']]

        # Rebuild the fields object in the desired order
        self.fields = self.fields.select(*reordered_fields)
     
def getUserDataSchema():
    portal = get_portal()
    form_name = "In User Profile"
    if getSecurityManager().checkPermission("Manage portal", portal):
        form_name = None
    schema = getSchema(IUserDataSchema, UserDataPanelAdapter, form_name=form_name)
    
    
    return schema

