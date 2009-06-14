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

def feedFormattedDate(dateToFormat):
	##Mon, 02 Jun 2008 10:32:32 EDT
	dateToFormat = dateToFormat - datetime.timedelta(hours=4)  # for eastern standard time
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
	ohhai = ("%s, %s %s%s, %s at %s%s:%s%s:%s%s" % (day(dateToFormat.isoweekday() - 1),month(dateToFormat.month),zeroDay,dateToFormat.day,dateToFormat.year,zeroHour,dateToFormat.hour,zeroMinute,dateToFormat.minute,zeroSecond,dateToFormat.second))
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







class MainHandler(webapp.RequestHandler):
	def get(self):
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
		#blogtitle = "Anderson Miller's Blog"
		#tagline = "I wrote this blog myself.  The Blog, not just the content."
		i = 0
		blogposts = ""
		for post in posts:
			i = i + 1
			if(post.published):
				title = post.title
				postdate = feedFormattedDate(post.date)
				postdate += " <strong>%s</strong> wrote:" % author
				img = ""
				if(post.image):
					img = "<div class=\"span-12 last\"><img src=\"/img?img_id=%s\"><br/></div>" % post.key()
				body = textile.textile(post.content)
				galleryCode = gallery.Gallery()
				galleryCode.constructGallery(post.post_id,False)
				body += galleryCode.render()
				template_values = {
					'title':title,
					'postdate':postdate,
					'img':img,
					'body':body
				}
				blogposts += template.render('newpost.html',template_values)
		
		
		template_values = {
			'title': blogtitle,
			'tagline':tagline, 
			'postbody' : blogposts,
			'website' : siteHome
		}
		self.response.out.write(template.render('frontpage.html',template_values))
		
class EditPost(webapp.RequestHandler):
	def get(self):
		postData = self.request.get('post')
		if(postData):
			postToEdit = int(postData)
			#self.response.out.write(postToEdit)
			post = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",postToEdit)
			for pos in post:
				galleryCode = gallery.Gallery()
				galleryCode.constructGallery(pos.post_id,True)
				self.response.out.write(template.render('edit.html',{'postNumber' : pos.post_id, 'title' : pos.title, 'content' : pos.content ,'gallery_code' : galleryCode.render(), 'renderedcontent' : textile.textile(pos.content)}))

		else:
			posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY post_id")
			for post in posts:
				self.response.out.write("Post %s: %s <a href=\"/edit?post=%s\">edit</a><br/>" % (post.post_id, post.title, post.post_id))
		
		
class Post(webapp.RequestHandler):
	def get(self):
		self.response.out.write("I'm where you post stuff!")
		self.response.out.write("""
	      <html>
	        <body>
	          <form action="/recieve" enctype="multipart/form-data"  method="post">
				<div><textarea name="title" rows="1" cols = "60"></textarea></div>
	            <div><textarea name="content" rows="3" cols="60"></textarea></div>
				<div><input type="file" name="img"/></div>
				<div>Publish <input type="checkbox" name="publish" value="1"></div>
	            <div><input type="submit" value="Post To Blog"></div>
	          </form>
	        </body>
	      </html>""")
	    
		
class Recieve(webapp.RequestHandler):
	def post(self):
		posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY date DESC")
		i = 0
		for post in posts:
			i += 1
		
		self.response.out.write("I am for putting posts into the database")
		post = common.BlogPost()
		post.post_id = i + 1
		post.content = self.request.get('content')
		post.title = self.request.get('title')
		image = self.request.get("img")
		post.published = bool(self.request.get('publish'))
		if(image):
			post.image = db.Blob(image)
		#if(publish):
		#	post.published = True
		post.put()
		self.redirect('/edit')

class TakeEdit(webapp.RequestHandler):
	def post(self):
		post_id = int(self.request.get('post_id'))
		post = db.GqlQuery("SELECT * FROM BlogPost WHERE post_id=:1",post_id)
		for pos in post:
			pos.content = self.request.get('content')
			pos.title = self.request.get('title')
			pos.put()
		self.redirect('/')


def main():
	application = webapp.WSGIApplication([('/', MainHandler),('/post',Post),('/recieve',Recieve),('/edit',EditPost),('/recieveedit',TakeEdit)],
                                       debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
