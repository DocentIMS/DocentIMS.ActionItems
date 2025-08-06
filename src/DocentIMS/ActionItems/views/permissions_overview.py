# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
# from zope.component.hooks import setSecurityManager
# from AccessControl.SecurityManagement import getSecurityManager
from AccessControl import SpecialUsers
from Products.CMFCore.utils import getToolByName
from plone import api
 
from AccessControl.SecurityManagement import getSecurityManager, setSecurityManager

 

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPermissionsOverview(Interface):
    """ Marker Interface for IPermissionsOverview"""

 
class PermissionsOverview(BrowserView):
    
    def portal(self):
        return api.portal.get()
    
    def portal_url(self):
        return api.portal.get().absolute_url()

    def get_user_permissions(self, obj, user_id):
        user = api.user.get(username=user_id)
        
        if not user:
            return None

        # user = user.__of__(plone.api.portal.get().acl_users)  # Wrap in acquisition
        old_sm = getSecurityManager()
        setSecurityManager(user)
        
        
        try:
            result = {
                'View':  api.user.has_permission('View', user=user, obj=obj),
                'Modify': api.user.has_permission('Modify portal content', user=user, obj=obj),
                'Delete': api.user.has_permission('Delete objects', user=user, obj=obj),
                'permissions' : api.user.get_permissions(user=user, obj=obj),
                'workflow_actions': self.get_available_workflow_actions(obj, user),
            }
            return result
        finally:
            setSecurityManager(old_sm)

    
    def get_available_workflow_actions(self, obj, user=None):
        """Returns workflow actions available to a user on an object"""
        portal = self.portal()
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

            
    def get_results(self):
        request = self.request
        uid = request.get('folder', None)
        if not uid:
            brains = api.content.find(context=self.context)       
        else:
            folder = api.content.get(UID=uid)    
            if not folder:
                return None
            brains = api.content.find(context=folder, sort_on='getObjPositionInParent', sort_order='descending')
            
        user_ids = self.get_users()
        results = []
        
        for brain in brains:
            obj = brain.getObject()
            row = {'title': obj.Title(), 'path': obj.getPhysicalPath(), 'url': obj.absolute_url(), 'users': {}}
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

        results = catalog(sort_on='sortable_title', portal_type=['Plone Site', 'Folder'])

        items = []
        for brain in results[:100]:  # limit for performance
            items.append({
                "uid": brain.UID,  
                "path": brain.getPath(),  # or brain.UID
                "text": brain.Title or brain.id
            })
            
        return items


