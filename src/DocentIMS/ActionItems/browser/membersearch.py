# from plone.autoform.form import AutoExtensibleForm
from plone.base import PloneMessageFactory as _
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
 
from plone.autoform import directives as form
from plone.autoform import directives
from z3c.form import interfaces
from z3c.form import button
 
from plone.app.users.browser.membersearch import IMemberSearchSchema
from plone.app.users.browser.membersearch import MemberSearchForm

from plone.app.z3cform.widget import AjaxSelectWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget

from zope.interface import provider
from zope import schema



# from z3c.form.widget import ComputedWidgetAttribute
# from plone.autoform.interfaces import IFormFieldProvider
# from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from plone import schema
# from plone.formwidget.autocomplete import AutocompleteFieldWidget
# from plone.app.z3cform.widget import SelectWidget
# from plone.app.z3cform.widget import SelectFieldWidget


import plone.app.users.browser.membersearch 


# @provider(IFormFieldProvider)
class IActionMemberSearchSchema(IMemberSearchSchema):
    """Provide schema for member search."""

    # fields=["login", "email", "fullname"],
    
    login = schema.Choice(
        title=_("label_name", default="Full Name"),
        description=_(
            "help_search_name", default="Use search criteria to find team members/ Select user to display a contact form and their created content"
        ),
        vocabulary="DocentIMS.ActionItems.TeamIdsVocabulary",
        required=False,
    )
    
    model.fieldset(
        "extra",
        # label=_("legend_member_search_criteria", default="User Search Criteria"),
         label=_("legend_none", default=""), 
    )
    
    # form.omitted('login') 
    form.omitted('email') 
    form.omitted('fullname') 
    directives.widget('login', AjaxSelectFieldWidget,   vocabulary="DocentIMS.ActionItems.TeamIdsVocabulary", description="Select user to display a contact form and their created content")
    # directives.widget('fullname', AjaxSelectFieldWidget,   vocabulary="DocentIMS.ActionItems.FullnamesVocabulary", description="Select user to display a contact form and their created content")
   
def extractCriteriaFromRequest(criteria):
    """Takes a dictionary of z3c.form data and sanitizes it to fit
    for a pas member search.
    """
    for key in [
        "_authenticator",
        "form.buttons.search",
        "form.widgets.roles-empty-marker",
    ]:
        if key in criteria:
            del criteria[key]
    for key, value in list(criteria.items()):
        if not value:
            del criteria[key]
        else:
            new_key = key.replace("form.widgets.", "")
            criteria[new_key] = value
            del criteria[key]

    return criteria   
    
class ActionMemberSearchForm(MemberSearchForm):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = IActionMemberSearchSchema
    
    # ignoreContext = True

    label = _("heading_member_search", default="Search for users and their content")
    description = _(
        "description_member_search",
        default="This search form enables you to find users by "
        "specifying one or more search criteria.",
    )
    template = ViewPageTemplateFile("action_membersearch_form.pt")
    
    
    @button.buttonAndHandler(_("label_search", default="Search"), name="search")
    def handleApply(self, action):
        request = self.request
        data, errors = self.extractData()
        
        if errors:
            self.status = self.formErrorsMessage
            return

        if request.get("form.buttons.search", None):
            self.submitted = True

            view = self.context.restrictedTraverse("@@pas_search")
            criteria = extractCriteriaFromRequest(self.request.form.copy())
            self.results = view.searchUsers(sort_by="fullname", **criteria)

            
  
            
            