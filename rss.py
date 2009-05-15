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



class RssFeed(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/xml'
		self.response.out.write("""<?xml version="1.0" encoding="utf-8"?><rss version="2.0">\n
		\t<channel>\n
		\t<link>http://blog.candersonmiller.com/</link>\n
		\t<description>Anderson Miller&apos;s blog.</description>\n
		\t<language>en-us</language>\n
		\t<managingEditor>candersonmiller@gmail.com (Anderson Miller)</managingEditor>\n
		\t<copyright>http://creativecommons.org/licenses/by-sa/1.0</copyright>\n
		\t\t<lastBuildDate>
		""")
		foodevents = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date DESC LIMIT 1")
		for foodevent in foodevents:
			foodevent.date = foodevent.date - datetime.timedelta(hours=4)
			
			zeroMinute = ""
			if(foodevent.date.minute < 10):
				zeroMinute = "0"
			zeroHour = ""
			if(foodevent.date.hour < 10):
				zeroHour = "0"
			zeroSecond = ""
			if(foodevent.date.second < 10):
				zeroSecond = "0"
			self.response.out.write('%s EDT' % common.feedFormattedDate(foodevent.date))
			#Mon, 02 Jun 2008 10:32:32 EDT
		self.response.out.write("""</lastBuildDate>\n

		\t\t<generator>http://www.movabletype.org/?v=3.2</generator>
		\t\t<webMaster>candersonmiller@gmail.com (Anderson Miller)</webMaster>
		\t\t<ttl>30</ttl>
		""")
		blogposts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date DESC LIMIT 10")
		for blogpost in blogposts:
			blogpost.date = blogpost.date - datetime.timedelta(hours=4)
			self.response.out.write('\t\t\t<entry>\n')
			content = cgi.escape(blogpost.content)
			self.response.out.write('\t\t\t\t<title>%s</title>\n' % blogpost.title )
			self.response.out.write('\t\t\t\t<description>%s <br/><img src="http://blog.candersonmiller.com/img?img_id=%s"></img></description>\n' % (content,blogpost.key()))
			self.response.out.write('\t\t\t\t<link>http://blog.candersonmiller.com/posts/%s</link>\n' % blogpost.post_id)
			self.response.out.write('\t\t\t\t<pubDate>%s -0500</pubDate>\n' % common.feedFormattedDate(foodevent.date))
			self.response.out.write('\t\t\t\t<author>candersonmiller@gmail.com</author>\n')
			self.response.out.write('\t\t\t</entry>\n')

		self.response.out.write("""
		
		</channel>
		</rss>
		

		""")
		

def main():
  application = webapp.WSGIApplication([('/rss',RssFeed)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

