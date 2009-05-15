#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import wsgiref.handlers
import cgi
import time
import datetime
import os
import array

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail

import common

def getLastBuildDate():
	blogposts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date DESC LIMIT 1")
	for blogpost in blogposts:
		return '%s EDT' % common.feedFormattedDate(blogpost.date)

def getPubDateFromDBDate(dateToConvert):
	return '%s EDT' % common.feedFormattedDate(dateToConvert)


class RssFeed(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/xml'
		lastBuildDate = getLastBuildDate()
		
		blogposts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date")
		entries = ""
		for blogpost in blogposts:
			entries += template.render('newRssEntry.xml',{'title': blogpost.title, 'description': blogpost.content, 'link' : "http://blog.candersonmiller.com/post/%d" % blogpost.post_id, 'pubDate' : getPubDateFromDBDate(blogpost.date)})
		
		
		self.response.out.write(template.render('atom.xml',{'entries':entries}))
		

def main():
  application = webapp.WSGIApplication([('/rss',RssFeed)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

