

from grokcore import component as grok
from grokcore.layout.interfaces import ILayout, IPage
from megrok import pagetemplate as pt
from zope import component
from zope.publisher.publish import mapply

from zeam.form.base.form import Form as BaseForm
from zeam.form.composed.form import ComposedForm as BaseComposedForm



class LayoutAwareForm(object):
    """A mixin to make form aware of layouts.
    """

    def __init__(self, context, request):
        super(LayoutAwareForm, self).__init__(context, request)
        self.layout = None

    def default_namespace(self):
        namespace = super(LayoutAwareForm, self).default_namespace()
        namespace['layout'] = self.layout
        return namespace

    def content(self):
        return self.render()

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue processing the form
            return

        self.updateForm()
        if self.request.response.getStatus() in (302, 303):
            return

        self.layout = component.getMultiAdapter(
            (self.request, self.context), ILayout)
        return self.layout(self)


class Form(LayoutAwareForm, BaseForm):
    """A zeam.form Form which is able to use a layout to render
    itself.
    """
    grok.baseclass()
    grok.implements(IPage)


class FormTemplate(pt.PageTemplate):
    """Template for a layout aware form.
    """
    pt.view(Form)


class ComposedForm(LayoutAwareForm, BaseComposedForm):
    """A composed zeam.form form which is able to use a layout to
    render itself.
    """
    grok.baseclass()
    grok.implements(IPage)


class ComposedFormTemplate(pt.PageTemplate):
    """Template for a layout aware composed form.
    """
    pt.view(ComposedForm)


