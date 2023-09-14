# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Acquisition import aq_inner
from DocentIMS.ActionItems import _
from plone import schema
from plone.app.portlets.portlets import base 
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer
from plone.app.layout.viewlets import ViewletBase
from plone import api




class IAddActionItemPortletPortlet(IPortletDataProvider):
    place_str = schema.TextLine(
        title=_(u'Button text'),
        required=True,
        default=u'Add Action Item'
    )


@implementer(IAddActionItemPortletPortlet)
class Assignment(base.Assignment):
    schema = IAddActionItemPortletPortlet

    @property
    def title(self):
        return _(u'Add action item')



class AddForm(base.AddForm):
    schema = IAddActionItemPortletPortlet
    form_fields = field.Fields(IAddActionItemPortletPortlet)
    label = _(u'Add Action item portlet')
    description = _(u'This portlet displays a button to add action items')

    def create(self, data):
        return Assignment(
            place_str=data.get('place_str', 'Add Action Item'),
        )


class EditForm(base.EditForm):
    schema = IAddActionItemPortletPortlet
    form_fields = field.Fields(IAddActionItemPortletPortlet)
    label = _(u'Edit Portlet')
    description = _(u'This portlet displays a button to add action items')


class Renderer(base.Renderer):
    schema = IAddActionItemPortletPortlet
    _template = ViewPageTemplateFile('add_action_item_portlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request),
            name=u'plone_portal_state'
        )
        self.anonymous = portal_state.anonymous()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements and
        not an anonymous user."""
        return not self.anonymous

    
    @property
    def portal_url(self):
        return api.portal.get().absolute_url() 
 