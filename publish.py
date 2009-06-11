#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by C. Anderson Miller on 2009-02-21.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import array
import time
import wsgiref.handlers
import common
import time
import datetime





class Publish(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		input_id = self.request.get("post_id")
		title = ""
		entry = ""
		number = int(input_id)
				
		self.response.out.write("published %d" % number)
		if(number > 0):
			posts = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",number)
			for post in posts:
				post.published = True
				post.put()


class UnPublish(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		input_id = self.request.get("post_id")
		title = ""
		entry = ""
		number = int(input_id)
		self.response.out.write("unpublished %d" % number)

		if(number > 0):
			posts = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",number)
			for post in posts:
				post.published = False
				post.put()

def main():
	application = webapp.WSGIApplication([('/publish',Publish),('/unpublish',UnPublish)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()