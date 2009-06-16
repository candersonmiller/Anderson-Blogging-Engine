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
	months = {
		1 : "Jan",
		2 : "Feb",
		3 : "Mar",
		4 : "Apr",
		5 : "May",
		6 : "Jun",
		7 : "Jul",
		8 : "Aug",
		9 : "Sep",
		10 : "Oct",
		11 : "Nov",
		12 : "Dec"
	}
	return months[num]


def day(num):
	days = {
		0 : "Mon",
		1 : "Tue",
		2 : "Wed",
		3 : "Thu",
		4 : "Fri",
		5 : "Sat",
		6 : "Sun"
	}
	return days[num]


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
	


