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





class PostEdit(webapp.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		input_id = self.request.get("id")
		title = ""
		entry = ""
		number = 0
		
		if(input_id[0:5] == "title"):
			title = self.request.get("value")
			number = int(input_id[5:])
			
		if(input_id[0:5] == "entry"):
			entry = self.request.get("value")
			number = int(input_id[5:])
		
		if(title):
			self.response.out.write("%s" % title)
			posts = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",number)
			for post in posts:
				post.title = title
				post.put()
				
		if(entry):
			self.response.out.write("%s" % entry)
			posts = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",number)
			for post in posts:
				post.content = entry
				post.put()

def main():
	application = webapp.WSGIApplication([('/postedit',PostEdit)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()