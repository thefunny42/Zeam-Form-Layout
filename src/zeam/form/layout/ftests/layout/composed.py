"""
We will define here a layout and render a composed form inside it.

First we need to grok our package:

  >>> from zeam.form.layout.testing import grok
  >>> grok('zeam.form.layout.ftests.layout.composed')

Now we can lookup our form:

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> from zeam.form.layout.ftests.layout.composed import World
  >>> context = World()

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='lifemanagement')
  >>> form
  <zeam.form.layout.ftests.layout.composed.LifeManagement object at ...>

We can render our form:

  >>> print form()
  <html>
     <head>
     </head>
     <body>
       <h1> Directly from our planet </h1>
       <div class="content">
    <h1>A form to manage a guy</h1>
    <div class="subforms">
      <div class="subform"><form action="http://127.0.0.1" method="post" enctype="multipart/form-data">
    <h2>Add some people to the world</h2>
    <div class="actions">
      <div class="action">
        <input type="submit" id="form-birthgiver-action-new" name="form.birthgiver.action.new" value="New" class="action" />
      </div>
    </div>
  </form>
  </div>
      <div class="subform"><form action="http://127.0.0.1" method="post" enctype="multipart/form-data">
  <BLANKLINE>
    <h2>Collect some dead people</h2>
    <div class="actions">
      <div class="action">
        <input type="submit" id="form-deathcollector-action-collect" name="form.deathcollector.action.collect" value="Collect" class="action" />
      </div>
    </div>
  </form>
     </div>
     </div>
     </div>
     </body>
  </html>


Our composed have its own layout as you can see, and subforms as well:

  >>> form.subforms
  [<zeam.form.layout.ftests.layout.composed.BirthGiver object at ...>,
   <zeam.form.layout.ftests.layout.composed.DeathCollector object at ...>]
  >>> form.layout
  <zeam.form.layout.ftests.layout.composed.WorldLayout object at ...>

This content is rendered by a special template of this package. Now
let's try out that form with a browser:

  >>> root = getRootFolder()
  >>> root['earth'] = context

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/earth/lifemanagement')

  >>> action = browser.getControl('New')
  >>> action
  <SubmitControl name='form.birthgiver.action.new' type='submit'>

  >>> action.click()
  >>> "A new guy is born" in browser.contents
  True
  >>> "We catch a bunch of folks" in browser.contents
  False

  >>> action = browser.getControl('Collect')
  >>> action
  <SubmitControl name='form.deathcollector.action.collect' type='submit'>

  >>> action.click()
  >>> "A new guy is born" in browser.contents
  False
  >>> "We catch a bunch of folks" in browser.contents
  True

Let's render the composed form with an form error:

  >>> from zeam.form.base.errors import Error
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='lifemanagement')

  >>> form.formErrors
  []
  >>> form.errors.append(Error('I am an Error', identifier=form.prefix))
  >>> len(form.formErrors)
  1

  >>> print form()
  <html>
     <head>
     </head>
     <body>
       <h1> Directly from our planet </h1>
       <div class="content">
    <h1>A form to manage a guy</h1>
    <div class="form-error">
      <ul>
        <li> I am an Error </li>
      </ul>
    </div>
    <div class="subforms">
      <div class="subform"><form action="http://127.0.0.1" method="post" enctype="multipart/form-data">
    <h2>Add some people to the world</h2>
    <div class="actions">
      <div class="action">
        <input type="submit" id="form-birthgiver-action-new" name="form.birthgiver.action.new" value="New" class="action" />
      </div>
    </div>
  </form>
  </div>
      <div class="subform"><form action="http://127.0.0.1" method="post" enctype="multipart/form-data">
    <h2>Collect some dead people</h2>
    <div class="actions">
      <div class="action">
        <input type="submit" id="form-deathcollector-action-collect" name="form.deathcollector.action.collect" value="Collect" class="action" />
      </div>
    </div>
  </form>
    </div>
    </div>
    </div>
     </body>
  </html>


"""

from grokcore import component as grok
from grokcore.layout import Layout
from zeam.form import layout as zeamform


class World(grok.Context):
    pass


class WorldLayout(Layout):
    grok.context(World)


class LifeManagement(zeamform.ComposedForm):

    label = u"A form to manage a guy"


class BirthGiver(zeamform.SubForm):
    zeamform.context(World)
    zeamform.view(LifeManagement)

    label = u"Add some people to the world"

    @zeamform.action("New")
    def newPeople(self):
        self.status = u"A new guy is born"


class DeathCollector(zeamform.SubForm):
    zeamform.view(LifeManagement)

    label = u"Collect some dead people"

    @zeamform.action("Collect")
    def collectPeople(self):
        self.status = u"We catch a bunch of folks"
