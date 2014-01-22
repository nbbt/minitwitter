'''
Created on Jan 21, 2014

@author: anya
'''
from setuptools import setup, find_packages
setup(name='minitwitter',
      packages=find_packages(),
      scripts = ["scripts/run_twitter.py"], 
      version=0.2)
