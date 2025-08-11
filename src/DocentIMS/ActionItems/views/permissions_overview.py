# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
# from zope.component.hooks import setSecurityManager
# from AccessControl.SecurityManagement import getSecurityManager
from AccessControl import SpecialUsers
from Products.CMFCore.utils import getToolByName
from plone import api
from DocentIMS.ActionItems.interfaces import IDocentimsSettings
from plone.api.exc import InvalidParameterError
from AccessControl.SecurityManagement import getSecurityManager, setSecurityManager

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPermissionsOverview(Interface):
    """ Marker Interface for IPermissionsOverview"""

 
class PermissionsOverview(BrowserView):

    def __call__(self):
        self.ikons = self.get_typeicons()
        self.portal = self.get_portal()
        self.portal_url = self.get_portal_url()
        return self.index()
        
    
    def get_portal(self):
        return api.portal.get()
    
    def get_portal_url(self):
        return self.portal.absolute_url()

    def get_user_permissions(self, obj, user_id):
        user = api.user.get(username=user_id)
        
        if not user:
            return None

        # user = user.__of__(plone.api.portal.get().acl_users)  # Wrap in acquisition
        old_sm = getSecurityManager()
        setSecurityManager(user)
        
        
        try:
            # Alternatively, revert to loop, but it looks slow
            AddFolders = api.user.has_permission('Add Folders', user=user, obj=obj)
            CopyorMove  = api.user.has_permission('Copy or Move', user=user, obj=obj)
            ChangePermissions = api.user.has_permission('Change permissions', user=user, obj=obj)
            DefinePermissions = api.user.has_permission('Define permissions', user=user, obj=obj)
            
            result = {
                'View':  api.user.has_permission('View', user=user, obj=obj),
                'Modify': api.user.has_permission('Modify portal content', user=user, obj=obj),
                'Delete': api.user.has_permission('Delete objects', user=user, obj=obj),
                'permissions' : [CopyorMove, ChangePermissions, AddFolders, DefinePermissions],
                'workflow_actions': self.get_available_workflow_actions(obj, user),
            }
            return result
        finally:
            setSecurityManager(old_sm)

    
    def get_available_workflow_actions(self, obj, user=None):
        """Returns workflow actions available to a user on an object"""
        portal = self.portal
        wf_tool = getToolByName(portal, 'portal_workflow')
        
        # Switch to the context of the user, if a specific user is provided
        if user:
            # Impersonate user
            with api.env.adopt_user(user=user):
                return [t['id'] for t in wf_tool.getTransitionsFor(obj)]
        else:
            # Use current user
            return [t['id'] for t in wf_tool.getTransitionsFor(obj)]

    def get_users(self):
        raw = self.request.get('users', [])
        if isinstance(raw, list):
            raw = raw[0] if raw else ''
        elif isinstance(raw, str):
            raw = raw
        else:
            raw = ''
        return [u.strip() for u in raw.split(',') if u.strip()]

    def get_typeicons(self):  
        # TO Do: Probably better to look up all contenttypes and their icons instead of doing this again and again.
        icons = dict()
        catalog = api.portal.get_tool("portal_catalog")
        # Query only the portal_type field
        types_in_catalog = catalog.uniqueValuesFor('portal_type')
        for the_type in types_in_catalog:
            type_lower =  the_type.lower().replace(" ", "_")   
            # Icons are defined in xml in registry / content type and does not contain spaces or Capital letters
            icon = "plone.icon.contenttype/" + type_lower            
            try:      
                icons[the_type] = api.portal.get_registry_record(icon)
            except (KeyError, InvalidParameterError):
                # Portal type does not have an icon
                icons[the_type] =  '++plone++bootstrap-icons/file-earmark-text.svg'
        return icons
                
    def get_results(self):        
        # Get the plone_layout view
        request = self.request
        uid = request.get('folder', None)
        if not uid:
            folder = self.context
            brains = api.content.find(folder)       
        else:
            folder = api.content.get(UID=uid)    
            if not folder:
                return None
            brains = api.content.find(context=folder, sort_on='getObjPositionInParent', sort_order='descending')
        
        
        folder_path_lenght = len(folder.getPhysicalPath())
            
        user_ids = self.get_users()
        results = []
        
        for brain in brains:
            obj = brain.getObject()
            path =  obj.getPhysicalPath()
            the_type = obj.Type()
            portal_type = obj.portal_type
            row = {'title': obj.Title(), 
                   'ikon': self.ikons[portal_type], 
                   'portal_type': the_type, 
                   'path':  path, 
                   'indent': len(path) - folder_path_lenght, 
                   'url': obj.absolute_url(), 
                   'users': {}}            
            for user_id in user_ids:
                user_id = user_id
                if user_id:
                    perms = self.get_user_permissions(obj, user_id)
                    if perms:
                        row['users'][user_id] = perms
                        user = api.user.get(username=user_id)
                        row['users'][user_id]['name'] =  user.getProperty('fullname', '') or user_id
            results.append(row)
        return results
    
    
    def get_folders(self):
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(sort_on='sortable_title', portal_type=['Folder'])
        items = []
        for brain in results[:100]:  # limit for performance
            items.append({
                "uid": brain.UID,  
                "path": brain.getPath(),  # or brain.UID
                "text": brain.Title or brain.id
            })
            
        return items


