from setuptools import setup, find_packages
import os

version = '0.3.1'

tests_require = [
    'zope.interface',
    'zope.app.wsgi',
    'zope.configuration',
    'zope.testing',
    'zeam.form.base [test]',
    ]

setup(name='zeam.form.layout',
      version=version,
      description="grokcore.layout support for zeam.form",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Programming Language :: Zope",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zeam form layout',
      author='Sylvain Viollon',
      author_email='thefunny@gmail.com',
      url='',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['zeam', 'zeam.form'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'zope.component',
        'zope.publisher',
        'grokcore.component',
        'grokcore.layout',
        'grokcore.chameleon',
        'zeam.form.base >= 1.0',
        'zeam.form.composed >= 1.2',
        'megrok.pagetemplate',
        ],
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
