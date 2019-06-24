from setuptools import setup

setup(
   name='ttrpg_core',
   version='0.0.1',
   description='A module for exploring ttrpg systems',
   author='Adam Haapala',
   author_email='adamhaapala@yahoo.com',
   packages=['ttrpg_core'],  #same as name
   install_requires=['numpy', 'matplotlib'], #external packages as dependencies
)
