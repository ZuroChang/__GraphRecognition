# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:18:40 2020

@author: ZuroChang
"""


from flask import Blueprint

main=Blueprint('main',__name__)

from . import views, errors