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
import textile




class Rendered(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		input_id = self.request.get("post_id")
		number = int(input_id)
		if(number > 0):
			posts = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",number)
			for post in posts:
				#self.response.out.write(post.content)
				self.response.out.write(textile.textile("%s" % post.content))
		#		post.published = True
		#		post.put()



def main():
	application = webapp.WSGIApplication([('/rendered',Rendered)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()