# -*- coding: utf-8 -*-
import csv
import io
import requests
from plone import api
from Products.Five import BrowserView
from zope.interface import Interface
from zope.schema import Bytes
from z3c.form import form, field, button
from plone.autoform import directives as form_directives
from plone.namedfile.file import NamedBlobImage



class IUsersImport(Interface):
    """ Marker Interface for IUsersImport"""

class ICSVImportFormSchema(Interface):
    csv_file = Bytes(
        title=u"CSV File",
        description=u"Upload a CSV file with user data",
        required=True
    )

# class UsersImport(BrowserView):
#     def __call__(self):



class UsersImport(form.Form):
    fields = field.Fields(ICSVImportFormSchema)
    ignoreContext = True
    label = u"Import Users from CSV"

    @button.buttonAndHandler(u"Import")
    def handleImport(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        file_data = data['csv_file']
        decoded = file_data.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))

        created_users = []
        for row in reader:
            email = row.get("email")
            if not email:
                continue  # skip if no email

            username = email.lower().strip()
            if api.user.get(username=username):
                continue  # skip existing

            user = api.user.create(
                username=username,
                email=email,
                password=api.portal.get_tool("portal_registration").generatePassword(),
                properties={
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "fullname": row.get("fullname"),
                    "cellphone": row.get("cellphone"),
                    "officephone": row.get("officephone"),
                    "your_team_role": row.get("your_team_role"),
                    "company": row.get("company"),
                    "notes": row.get("notes"),
                }
            )

            # Handle portrait (URL or local path)
            portrait_url = row.get("portrait")
            if portrait_url:
                try:
                    if portrait_url.startswith("http"):
                        resp = requests.get(portrait_url)
                        if resp.status_code == 200:
                            img_data = NamedBlobImage(data=resp.content,
                                                      filename=u"portrait.jpg")
                            user.setMemberProperties({'portrait': img_data})
                    # Local file handling could be added here
                except Exception:
                    pass

            created_users.append(username)

        self.status = f"Imported {len(created_users)} users: {', '.join(created_users)}"
