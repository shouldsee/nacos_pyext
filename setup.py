#!/usr/bin/env python
#from setuptools import setup
from distutils.core import setup
#import setuptools
import os,glob,sys

setup(
	name='nacos_pyext',
	version='v0.0.1',
	packages=['.'],
  include_package_data=True,    
	license='Apache2.0',
	author='Feng Geng',
	author_email='shouldsee@qq.com',
	#long_description=open('README.md').read(),
	install_requires=[
  'nacos-sdk-python==0.1.7',
#		x.strip() for x in open("requirements.txt","r") 
#        	if x.strip() and not x.strip().startswith("#") 
	],

)
