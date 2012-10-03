"""
We will define here a layout and render a form inside it.

First we need to grok our package:

  >>> from zeam.form.layout.testing import grok
  >>> grok('zeam.form.layout.ftests.layout.form')

Now we can lookup our form:

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> from zeam.form.layout.ftests.layout.form import Guy
  >>> context = Guy()

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='helloform')
  >>> form
  <zeam.form.layout.ftests.layout.form.HelloForm object at ...>

We can render our form:

  >>> print form()
  <html>
    <head>
    </head>
    <body>
      <h1> This is a cool layout for a guy </h1>
      <div class="content"><form action="http://127.0.0.1" method="post"
                                 enctype="multipart/form-data">
          <h1>A form about a guy</h1>
          <div class="actions">
            <div class="action">
               <input type="submit" id="form-action-say-hello"
                      name="form.action.say-hello" value="Say hello" class="action" />
            </div>
          </div>
        </form>
      </div>
    </body>
  </html>

You can get the content to be inserted inside the layout/the layout
from here:

  >>> print form.content()
  <form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data">
      <h1>A form about a guy</h1>
      <div class="actions">
          <div class="action">
              <input type="submit" id="form-action-say-hello"
                     name="form.action.say-hello" value="Say hello" class="action" />
          </div>
      </div>
  </form>

  >>> form.layout
  <zeam.form.layout.ftests.layout.form.GuyLayout object at ...>

This content is rendered by a special template of this package. Now
let's try out that form with a browser:

  >>> root = getRootFolder()
  >>> root['guy'] = context

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/guy/helloform')

  >>> action = browser.getControl('Say hello')
  >>> action
  <SubmitControl name='form.action.say-hello' type='submit'>

  >>> action.click()
  >>> print browser.contents
  <html>
    <head>
    </head>
    <body>
      <h1> This is a cool layout for a guy </h1>
      <div class="content"><form action="http://localhost/guy/helloform" method="post"
                                 enctype="multipart/form-data">
          <h1>A form about a guy</h1>
          <p class="form-status">Hello</p>
          <div class="actions">
             <div class="action">
                <input type="submit" id="form-action-say-hello"
                       name="form.action.say-hello" value="Say hello" class="action" />
             </div>
          </div>
        </form>
      </div>
    </body>
  </html>

Now we render the form with an form error:

  >>> from zeam.form.base.errors import Error
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='helloform')

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
       <h1> This is a cool layout for a guy </h1>
       <div class="content"><form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data">
    <h1>A form about a guy</h1>
    <div class="form-error">
      <ul>
        <li> I am an Error </li>
      </ul>
    </div>
    <div class="actions">
      <div class="action">
        <input type="submit" id="form-action-say-hello" name="form.action.say-hello" value="Say hello" class="action" />
      </div>
    </div>
  </form>
  </div>
     </body>
  </html>

"""

from grokcore import component as grok
from grokcore.layout import Layout
from zeam.form import layout as zeamform


class Guy(grok.Context):
    pass


class GuyLayout(Layout):
    grok.context(Guy)


class HelloForm(zeamform.Form):

    label = u"A form about a guy"

    @zeamform.action("Say hello")
    def sayHello(self):
        self.status = u"Hello"

