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

#import GMap



class Settings(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		settings = db.GqlQuery("SELECT * FROM SiteSettings")
		blogName = ""
		blogSaying = ""
		siteHome = ""
		author = ""
		i = 0
		for setting in settings:
			blogName = setting.blogName
			blogSaying = setting.blogSaying
			siteHome = setting.siteHome
			author = setting.author
			#self.response.out.write("counts!")
			if(i == 1):
				setting.delete()
			i += 1	
		
		template_values = {
			'blogName' : blogName,
			'blogSaying' : blogSaying,
			'siteHome': siteHome,
			'author': author
		}
			
		self.response.out.write(template.render('settings.html',template_values))
			
class SubmitSettings(webapp.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		#self.response.out.write(blogName)
		input_id = self.request.get("id")
		#self.response.out.write(input_id)
		blogName = ""
		blogSaying = ""
		siteHome = ""
		author = ""
		if(input_id == "blogName"):
			blogName = self.request.get("value")
			
		if(input_id == "blogSaying"):
			blogSaying = self.request.get("value")
		
		if(input_id) == "siteHome":
			siteHome = self.request.get("value")
			
		if(input_id) == "author":
			author = self.request.get("value")
		
		if(blogName):
			self.response.out.write("%s" % blogName)
			settings = db.GqlQuery("SELECT * FROM SiteSettings")
			i = 0
			for setting in settings:
				if i > 0:
					setting.delete()
				else:
					setting.blogName = blogName
					setting.put()
				i = i + 1
				
		if(blogSaying):
			self.response.out.write("%s" % blogSaying)
			settings = db.GqlQuery("SELECT * FROM SiteSettings")
			i = 0
			for setting in settings:
				if i > 0:
					setting.delete()
				else:
					setting.blogSaying = blogSaying
					setting.put()
				i = i + 1
				
		if(siteHome):
			self.response.out.write("%s" % siteHome)
			settings = db.GqlQuery("SELECT * FROM SiteSettings")
			i = 0
			for setting in settings:
				if i > 0:
					setting.delete()
				else:
					setting.siteHome = siteHome
					setting.put()
				i = i + 1
				
		
		if(author):
			self.response.out.write("%s" % author)
			settings = db.GqlQuery("SELECT * FROM SiteSettings")
			i = 0
			for setting in settings:
				if i > 0:
					setting.delete()
				else:
					setting.author = author
					setting.put()
				i = i + 1

def main():
	application = webapp.WSGIApplication([('/settings',Settings),('/settingssubmit',SubmitSettings)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()