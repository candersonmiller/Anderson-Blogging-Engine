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
import datetime

import common
import textile
import gallery
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app




class History(webapp.RequestHandler):
	def get(self,pageNumber):
		if(int(pageNumber) == 0):
			self.redirect('/')
		self.response.headers['Content-Type'] = 'text/html'
		posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date DESC")
		
		settings = db.GqlQuery("SELECT * FROM SiteSettings")
		blogtitle = ""
		tagline = ""
		author = ""
		siteHome = ""
		i = 0
		for setting in settings:
			blogtitle = setting.blogName
			tagline = setting.blogSaying
			author = setting.author
			siteHome = setting.siteHome
			i += 1
		
		if( i == 0):
			setting = common.SiteSettings()
			setting.blogName = "placeholder"
			setting.blogSaying = "placeholder"
			setting.author = "placeholder"
			setting.siteHome = "http://www.candersonmiller.com/"
			setting.put()



		i = 0
		j = 0
		onFrontPage = 0
		blogposts = ""
		next_number = int(pageNumber) - 1
		previous_number = int(pageNumber) + 1
		for post in posts:
			i = i + 1
			if( j > (int(pageNumber) * 5) and post.published and (onFrontPage < 5)):
				onFrontPage = onFrontPage + 1
				title = post.title
				postdate = common.feedFormattedDate(post.date)
				postdate += " <strong>%s</strong> wrote:" % author
				img = ""
				if(post.image):
					img = "<div class=\"span-12 last\"><img src=\"/img?img_id=%s\"><br/></div>" % post.key()
				body = textile.textile(post.content)
				galleryCode = gallery.Gallery()
				galleryCode.constructGallery(post.post_id,False,False)
				body += galleryCode.render()
				template_values = {
					'title':title,
					'postdate':postdate,
					'img':img,
					'body':body
				}
				blogposts += template.render('newpost.html',template_values)
		
			if(post.published):
				j = j + 1
				
		template_values = {
			'title': blogtitle,
			'tagline':tagline, 
			'postbody' : blogposts,
			'website' : siteHome,
			'next_number' : next_number,
			'previous_number' : previous_number
		}
		self.response.out.write(template.render('history.html',template_values))
		



def main():
	application = webapp.WSGIApplication([(r'/history/(.*)', History)],
                                       debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
