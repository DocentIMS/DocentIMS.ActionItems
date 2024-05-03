# from plone.autoform.form import AutoExtensibleForm
from plone.base import PloneMessageFactory as _
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
 
from plone.autoform import directives as form
 

from plone.app.users.browser.membersearch import IMemberSearchSchema
from plone.app.users.browser.membersearch import MemberSearchForm
from plone.autoform import directives
from plone.app.z3cform.widget import AjaxSelectWidget
# from plone.app.z3cform.widget import SelectWidget
# from plone.app.z3cform.widget import SelectFieldWidget


import plone.app.users.browser.membersearch 


class IActionMemberSearchSchema(IMemberSearchSchema):
    """Provide schema for member search."""

    # fields=["login", "email", "fullname"],
    # hide fields here
    # form.widget['login'].mode = interfaces.HIDDEN_MODE
    # form.widget['email'].mode = interfaces.HIDDEN_MODE
    # pass
    
    model.fieldset(
        "extra",
        label=_("legend_member_search_criteria", default="User Search Criteria"),
    )
    
    form.omitted('login') 
    form.omitted('email') 
    directives.widget(
        "fullname", AjaxSelectWidget,  
        select_displayed="exact",
        select_limit=1,
        allow_multiple=False, 
        vocabulary="plone.app.vocabularies.Users"
    )
    
    
     
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
    # template = ViewPageTemplateFile("action_membersearch_form.pt")

            
  
            
            