# -*- coding: utf-8 -*-

# from DocentIMS.ActionItems import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from plone import api
# from plone.contentrules.engine.interfaces import IRuleStorage
# from zope.component import queryMultiAdapter
# from zope.component import queryUtility
# from plone.app.contentrules.handlers import execute

from Acquisition import aq_inner
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IMailSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from Products.statusmessages.interfaces import IStatusMessage
# from zope import schema
from zope.component import adapter, getUtility
from zope.interface.interfaces import ComponentLookupError
# from zope.globalrequest import getRequest
from zope.interface import implementer, Interface
from plone import api
from datetime import datetime
from DocentIMS.ActionItems.interfaces import IDocentimsSettings
from plone.protect.utils import safeWrite
# from plone.protect.utils import addTokenToUrl
# from plone.protect.interfaces import IDisableCSRFProtection
# from zope.interface import alsoProvides





now = datetime.now()

import logging
logger = logging.getLogger(__file__)



class IReindexView(Interface):
    """ Marker Interface for IProjectView"""


class ReindexView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    #template = ViewPageTemplateFile('reindex_view.pt')

    # def __call__(self):
    #     # Implement your own actions:
    #     #return self.reindex()
    #     return self.index()
    
    def current_time(self):
        current_time = now.strftime("%H:%M:%S")
        return  current_time
    
    # def set_oldurgency(self, urgency)


    def reindex(self):
        my_brains = self.context.portal_catalog(portal_type=['action_items', 'sow_analysis'])
        # red = api.portal.get_registry_record('urgent_red', interface=IDocentimsSettings)
        
        registry = getUtility(IRegistry)
        self.mail_settings = registry.forInterface(IMailSchema, prefix="plone")
        #interpolator = IStringInterpolator(obj)

        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            abc = 1
            raise ComponentLookupError(
                "You must have a Mailhost utility to \
            execute this action"
            )

        self.email_charset = self.mail_settings.email_charset
        
        for brain in my_brains:
            obj = brain.getObject()
            #import pdb; pdb.set_trace()
            old_urgency = brain.urgency
            
            
            #import pdb; pdb.set_trace;
            #if not hasattr(obj, 'urgency'):
            #    import pdb; pdb.set_trace;
            #    obj.urgency = old_urgency
            
            if hasattr(obj, 'urgency'):
                
                old_urgency = obj.urgency
                
                
                daysleft = brain.daysleft
                obj.reindexObject(idxs=["daysleft", "urgency"])
                
                #Send mail if urgency changed
                if brain.urgency != old_urgency:
                    #Send email to user assigned
                    #print('we will send')
                    if brain.assigned_to:
                        #import pdb; pdb.set_trace()
                        object = brain.getObject()
                        interpolator = IStringInterpolator(object)
                        
                        assigned_user =  api.user.get(userid=brain.getObject().assigned_to)
                        self.recipients = assigned_user.getProperty('email')
                        
                        if self.recipients:
                            # print('sending mail')
                            
                            melding = """<p>Hello ${assignedfullname}<p> <p>This is a friendly reminder that:  <a href="${absolute_url}">${title}</a>  is due in <b>${daysleft} work-days</b>.   </p>
                            <p>If you believe that you will get <a href="${absolute_url}">${title}</a> done in time, no action is required.</p>
                            <p>However,  
                            if you believe that you may miss the due date, please contact the project manager.</p><hr/> 
                            <p>Sincerely, <b>-</b></p>
                            <p>Project Manager<br/> ${project_short_name}</p>
                            </p>""" 
                            # prepend interpolated message with \n to avoid interpretation
                            # of first line as header
                            message = f"\n{interpolator(melding)!s}"
                            outer = MIMEMultipart('alternative')
                            outer['To'] = self.recipients
                            outer['From'] = self.mail_settings.email_from_address
                            outer['Subject'] =  "Item due"
                            outer.epilogue = ''
                            html_part = MIMEMultipart('related')
                            html_text = MIMEText(message, 'html', _charset='UTF-8')
                            html_part.attach(html_text)
                            outer.attach(html_part)
                            mailhost.send(outer.as_string())
                            # # Finally send mail.
                            mailhost.send(outer.as_string())
                            

                
            safeWrite(obj, self.request)
            obj.urgency  = brain.urgency
            obj.daysleft = brain.daysleft
     
            
        return len(my_brains)
        