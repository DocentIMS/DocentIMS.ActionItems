# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api


class CSSViewlet(ViewletBase):

    def color(self):
    	return api.portal.get_registry_record('DocentIMS.ActionItems.interfaces.IDocentimsSettings.color1')
        
    def index(self):
        return super(CSSViewlet, self).render()

 
    
