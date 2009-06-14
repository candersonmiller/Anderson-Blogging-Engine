#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by C. Anderson Miller on 2009-05-14.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import wsgiref.handlers
import cgi
import time
import datetime
import os
import array
import urllib
import base64 
from xml.dom import minidom

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import urlfetch


def feedFormattedDate(dateToFormat):
	##Mon, 02 Jun 2008 10:32:32 EDT
	zeroMinute = ""
	if(dateToFormat.minute < 10):
		zeroMinute = "0"
	zeroHour = ""
	if(dateToFormat.hour < 10):
		zeroHour = "0"
	zeroSecond = ""
	if(dateToFormat.second < 10):
		zeroSecond = "0"
	zeroDay = ""
	if(dateToFormat.day < 10):
		zeroDay = "0"
	ohhai = ("%s, %s%s %s %s %s%s:%s%s:%s%s" % (day(dateToFormat.isoweekday() - 1),zeroDay,dateToFormat.day,month(dateToFormat.month),dateToFormat.year,zeroHour,dateToFormat.hour,zeroMinute,dateToFormat.minute,zeroSecond,dateToFormat.second))
	return ohhai


def month(num):
	if(num == 1):
		return "Jan"
	if(num == 2):
		return "Feb"
	if(num == 3):
		return "Mar"
	if(num == 4):
		return "Apr"
	if(num == 5):
		return "May"
	if(num == 6):
		return "Jun"
	if(num == 7):
		return "Jul"
	if(num == 8):
		return "Aug"
	if(num == 9):
		return "Sep"
	if(num == 10):
		return "Oct"
	if(num == 11):
		return "Nov"
	if(num == 12):
		return "Dec"


def day(num):
	if(num == 0):
		return "Mon"
	if(num == 1):
		return "Tue"
	if(num == 2):
		return "Wed"
	if(num == 3):
		return "Thu"
	if(num == 4):
		return "Fri"
	if(num == 5):
		return "Sat"
	if(num == 6):
		return "Sun"


class BlogPost(db.Model):
	post_id = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	title = db.StringProperty()
	content = db.TextProperty()
	image = db.BlobProperty()
	published = db.BooleanProperty(default=False)
	
class ImagePost(db.Model):
	post_id = db.IntegerProperty()
	image_id = db.IntegerProperty()
	image = db.BlobProperty()
	thumbnail = db.BlobProperty()
	published = db.BooleanProperty(default=True)
	title = db.StringProperty(default="Image")
	
class SiteSettings(db.Model):
	blogName = db.StringProperty()
	blogSaying = db.StringProperty()
	siteHome = db.StringProperty()
	author = db.StringProperty()
	


