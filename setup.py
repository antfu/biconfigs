import os
from setuptools import setup

with open(os.path.join('biconfigs','__version__.py'), 'r') as f:
    version=f.read().strip().split('=')[-1].strip("' ")

setup(name='biconfigs',
      version=version,
      description='A file-object two way configs helper',
      url='https://github.com/antfu/biconfigs',
      author='Anthony Fu',
      author_email='anthonyfu117@hotmail.com',
      license='MIT',
      packages=['biconfigs'],
      zip_safe=False)
