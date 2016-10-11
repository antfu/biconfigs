import os
import codecs
from setuptools import setup

def read(fname):
    try:
        with codecs.open(fname, 'r', 'utf-8') as f:
            return f.read()
    except IOError:
        return ""

try:
    from pypandoc import convert
except ImportError:
    # failed to load pypandoc, use the orginal markdown
    convert = lambda fname, to: read(fname)

version=read(os.path.join('biconfigs','__version__.py')).strip().split('=')[-1].strip("' ")

setup(name='biconfigs',
      version=version,
      description='Two way configurations mapping helper for Python.',
      url='https://github.com/antfu/biconfigs',
      author='Anthony Fu',
      keywords=['config','configuration','json'],
      author_email='anthonyfu117@hotmail.com',
      license='MIT',
      long_description=convert('README.md','rst'),
      packages=['biconfigs'],
      extras_require = {
        'cson':  ["cson"]
      },
      
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development',

          'License :: OSI Approved :: MIT License',

          # Python versions
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],)
