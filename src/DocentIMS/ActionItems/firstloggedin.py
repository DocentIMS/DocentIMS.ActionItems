from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm

from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
#from Products.statusrel_urls.interfaces import IStatusMessage
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from plone import api



 



class IRedirectAction(Interface):
    """Interface for the configurable aspects of a FirstLoggedin action.

    This is also used to create add and edit forms, below.
    """

    rel_url = schema.ASCIILine(
        title=_("Page to redirect to"),
        description=_("Where to send users. No first slash (/)"),
        required=True,
    )




@implementer(IRedirectAction, IRuleElementData)
class RedirectAction(SimpleItem):
    """The actual persistent implementation of the Redirectaction element."""

    rel_url = ""
    element = "DocentIMS.ActionItems.Redirect"
    
    #Redirect user here
    

    @property
    def summary(self):
        return _(
            "Redirect to ${rel_url}",
            mapping=dict(rel_url=self.rel_url),
        )


@adapter(Interface, IRedirectAction, Interface)
@implementer(IExecutable)
class RedirectActionExecutor:
    """The executor for this action.
    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        rel_url = _(self.element.rel_url)
        #rel_url_type = self.element.rel_url_type
        #request.response.redirect('/news')
        url = api.portal.get().absolute_url() + rel_url
        request.RESPONSE.redirect(url)
        #IStatusMessage(request).addStatusMessage(url, type=rel_url_type)
        # To do
        #request = self.REQUEST
        #self.context.REQUEST.RESPONSE.redirect('/news')

        return True 
        

class RedirectAddForm(ActionAddForm):
    """An add form for FirstLoggedin rule actions."""

    schema = IRedirectAction
    label = _("Redirect relative url")
    description = _("Redirects user to relative URI.")
    form_name = _("Configure element")
    Type = RedirectAction


class RedirectAddFormView(ContentRuleFormWrapper):
    form = RedirectAddForm


class RedirectEditForm(ActionEditForm):
    """An edit form for Redirect rule actions.

    z3c.form does all the magic here.
    """

    schema = IRedirectAction
    label = _("Edit FirstLoggedin Action")
    description = _("A FirstLoggedin action can show a rel_url to the user.")
    form_name = _("Configure element")


class RedirectEditFormView(ContentRuleFormWrapper):
    form = RedirectAddForm