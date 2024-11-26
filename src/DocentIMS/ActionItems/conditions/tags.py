from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from Products.CMFCore.Expression import createExprContext
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from z3c.form import form
from zope import schema
from plone.autoform import directives 
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
# from plone.supermodel import model
 
from plone.app.z3cform.widgets.select import AjaxSelectFieldWidget

# subjects



class ITagsCondition(Interface):
    """Interface for the configurable aspects of a TAG condition.

    This is also used to create add and edit forms, below.
    """
    
    # directives.widget(
    #     "subjects", AjaxSelectFieldWidget, vocabulary="plone.app.vocabularies.Keywords"
    # )
    subjects = schema.Tuple(
        title=_("label_tags", default="Tags"),
        description=_(
            "help_tags",
            default="Tags are commonly used for ad-hoc organization of " + "content.",
        ),
        value_type=schema.TextLine(),
        required=True,
        missing_value=(),
    )
    directives.widget(
         "subjects", AjaxSelectFieldWidget, vocabulary="plone.app.vocabularies.Keywords"
    )
    
 
@implementer(ITagsCondition, IRuleElementData)
class TagsCondition(SimpleItem):
    """The actual persistent implementation of the TAGS condition
    element.
    """

    subjects = ""
    element = "plone.conditions.Tags"

    @property
    def summary(self):
        return _(
            "TAGS is: ${subjects}",
            mapping={"subjects": self.subjects},
        )


@implementer(IExecutable)
@adapter(Interface, ITagsCondition, Interface)
class TagsConditionExecutor:
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        object = self.event.object
        subjects = self.element.subjects
        # Specify the tags to check for  
        tags = object.Subject()
        
        # Check if the object's tags contains tag
        # Later we probably do a loop or a lookup
        for tag in tags:
            return tag in subjects
        return False
    


class TagsAddForm(AddForm):
    """An add form for tag expression condition."""

    schema = ITagsCondition
    label = _("Add TAG Condition")
    description = _(
        "A TAG condition makes the rule apply "
        "only if TAG is not False in context."
    )
    form_name = _("Configure element")

    def create(self, data):
        c = TagsCondition()
        form.applyChanges(self, c, data)
        return c


class TagsAddFormView(ContentRuleFormWrapper):
    form = TagsAddForm


class TagsEditForm(EditForm):
    """An edit form for TAG condition"""

    schema = ITagsCondition
    label = _("Edit Tag Condition")
    description = _(
        "A TAGS condition makes the rule apply "
        "only if TAG is not False in context."
    )
    form_name = _("Configure element")


class TagsEditFormView(ContentRuleFormWrapper):
    form = TagsEditForm