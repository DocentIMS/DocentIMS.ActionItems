# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api

class AddActionItemViewlet(ViewletBase):

    #def update(self):
    #    self.message = self.get_message()

    #def get_message(self):
    #    return u'My message'

    def portal_url(self):
        return api.portal.get().absolute_url()

    def index(self):
        return super(AddActionItemViewlet, self).render()
