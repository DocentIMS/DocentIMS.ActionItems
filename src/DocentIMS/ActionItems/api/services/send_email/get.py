# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from AccessControl.Permissions import use_mailhost_services
from plone.registry.interfaces import IRegistry
from plone.restapi import _
from plone.restapi.bbb import IMailSchema
from plone.restapi.bbb import ISiteSchema
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from smtplib import SMTPException
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from Products.CMFPlone.utils import safe_unicode
import requests
import plone
from plone import api
import json
from io import BytesIO
from docx import Document


try:
    # Products.MailHost has a patch to fix quoted-printable soft line breaks.
    # See https://github.com/zopefoundation/Products.MailHost/issues/35
    from Products.MailHost.MailHost import message_from_string
except ImportError:
    # If the patch is ever removed, we fall back to the standard library.
    from email import message_from_string

class SendEmail(Service):
    def reply(self):
        data = json_body(self.request)
        send_to_address = data.get("to")
        uid = data.get("fileUid")
        sender_fullname = 'Docent IMS'
        item = api.content.get(UID=uid)
        subject = item.Title() or "File from Docent IMS"
        item_url = item.absolute_url()
        message_body = f"The file you requested: {item_url} \n\n"

        if not send_to_address:
            self.request.response.setStatus(400)
            return dict(error=dict(
                type="BadRequest",
                message='Missing "to" parameter.'
            ))

        overview_controlpanel = getMultiAdapter(
            (self.context, self.request), name="overview-controlpanel"
        )
        if overview_controlpanel.mailhost_warning():
            self.request.response.setStatus(400)
            return dict(error=dict(
                type="BadRequest",
                message="MailHost is not configured."
            ))

        sm = getSecurityManager()
        if not sm.checkPermission("plone.app.controlpanel.MailHost: UseMailHostServices", self.context):
            pm = getToolByName(self.context, "portal_membership")
            error_type = "Unauthorized" if pm.isAnonymousUser() else "Forbidden"
            self.request.response.setStatus(401 if error_type == "Unauthorized" else 403)
            return dict(error=dict(type=error_type, message="Access denied."))

        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix="plone")
        from_address = mail_settings.email_from_address
        encoding = registry.get("plone.email_charset", "utf-8")
        host = getToolByName(self.context, "MailHost")

        site_settings = registry.forInterface(ISiteSchema, prefix="plone", check=False)
        portal_title = site_settings.site_title or "Plone Site"

        # --- Create MIME email ---
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = send_to_address
        msg["Subject"] = safe_unicode(subject)
        msg.attach(MIMEText(message_body, "plain", encoding))

        # --- Try to attach file from URL ---
        try:
            # Get the file field
            file_field = getattr(item, "file", None)
            if not file_field or not getattr(file_field, "data", None):
                raise ValueError("Item has no file data")

            file_data = file_field.data
            filename = getattr(file_field, "filename", item.getId()) or "attachment"
            if file_field and getattr(file_field, "contentType", None) == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' :
            # if filename.lower().endswith(".docx"):
                try:
                    doc = Document(BytesIO(file_data))
                    props = doc.core_properties
                    props.title = item.Title() or "File from Docent IMS"
                    props.keywords = "Plone, Docent IMS"

                    buffer = BytesIO()
                    doc.save(buffer)
                    file_data = buffer.getvalue()
                except Exception as e:
                    # You can safely log or ignore metadata errors
                    pass
            

            # Create MIME attachment
            part = MIMEApplication(file_data)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"'
            )
            msg.attach(part)
        
        except Exception as e:
            return dict(error=dict(
                type="AttachmentError",
                message=f"Could not fetch file from {item_url}: {e}"
            ))

        # --- Send via MailHost ---
        try:
            host.send(
                msg.as_string(),
                mto=send_to_address,
                mfrom=from_address,
                subject=safe_unicode(subject),
                charset=encoding,
            )
        
        except (SMTPException, RuntimeError):
            plone_utils = getToolByName(self.context, "plone_utils")
            exception = plone_utils.exceptionString()
            message = f"Unable to send mail: {exception}"

            self.request.response.setStatus(500)
            return dict(error=dict(type="InternalServerError", message=message))

        return self.reply_no_content()
