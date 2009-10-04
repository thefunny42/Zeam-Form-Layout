"""
We will define here a layout and render a form inside it.

First we need to grok our package:

  >>> from zeam.form.layout.testing import grok
  >>> grok('zeam.form.layout.ftests.layout.layout')

Now we can lookup our form:

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> from zeam.form.layout.ftests.layout.layout import Guy
  >>> context = Guy()

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='helloform')
  >>> form
  <zeam.form.layout.ftests.layout.layout.HelloForm object at ...>

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
            <input type="submit" id="form-say-hello"
                   name="form.say-hello" value="Say hello" />
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
          <input type="submit" id="form-say-hello"
                 name="form.say-hello" value="Say hello" />
      </div>
  </form>

  >>> form.layout
  <zeam.form.layout.ftests.layout.layout.GuyLayout object at ...>

This content is rendered by a special template of this package. Now
let's try out that form with a browser:

  >>> root = getRootFolder()
  >>> root['guy'] = context

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/guy/helloform')

  >>> action = browser.getControl('Say hello')
  >>> action
  <SubmitControl name='form.say-hello' type='submit'>

  >>> action.click()
  >>> print browser.contents
  <html>
    <head>
    </head>
    <body>
      <h1> This is a cool layout for a guy </h1>
      <div class="content"><form action="http://localhost/guy/helloform" method="post"
                                 enctype="multipart/form-data">
          <p class="status-message">Hello</p>
          <h1>A form about a guy</h1>
          <div class="actions">
            <input type="submit" id="form-say-hello"
                   name="form.say-hello" value="Say hello" />
          </div>
        </form>
      </div>
    </body>
  </html>


"""

from megrok.layout import Layout
from zeam.form.layout import Form
from zeam.form.base import action

from grokcore import component as grok


class Guy(grok.Context):
    pass


class GuyLayout(Layout):
    pass


class HelloForm(Form):

    label = u"A form about a guy"

    @action("Say hello")
    def sayHello(self):
        self.status = u"Hello"

