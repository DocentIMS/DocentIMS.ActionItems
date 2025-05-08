# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Acquisition import aq_inner
from DocentIMS.ActionItems import _
from plone import schema
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer

import json
import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.request


class IReadunreadPortlet(IPortletDataProvider):
    place_str = schema.TextLine(
        title=_(u'Name of'),
        required=True,
        default=u'Show'
    )


@implementer(IReadunreadPortlet)
class Assignment(base.Assignment):
    schema = IReadunreadPortlet

    def __init__(self, place_str='Show'):
        self.place_str = place_str.lower()

    @property
    def title(self):
        return _(u'Show')


class AddForm(base.AddForm):
    schema = IReadunreadPortlet
    form_fields = field.Fields(IReadunreadPortlet)
    label = _(u'Add Portlet') 

    def create(self, data):
        return Assignment(
            place_str=data.get('place_str', 'Show'),
        )


class EditForm(base.EditForm):
    schema = IReadunreadPortlet
    form_fields = field.Fields(IReadunreadPortlet)
    label = _(u'Edit Show') 


class Renderer(base.Renderer):
    schema = IReadunreadPortlet
    _template = ViewPageTemplateFile('readunread.pt')

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

   
