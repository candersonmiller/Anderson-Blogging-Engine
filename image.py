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
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


def findImageIdNumber(post_id):
	imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id DESC LIMIT 1",post_id)
	image_id = 0
	for ip in imagePosts:
		image_id = ip.image_id + 1
	return image_id

	    

class Image (webapp.RequestHandler):
	def get(self):
		blogPost = db.get(self.request.get("img_id"))
		if blogPost.image:
			self.response.headers['Content-Type'] = "image/png"
			self.response.out.write(blogPost.image)
		else:
			self.error(404)
			
class FullImageRender (webapp.RequestHandler):
	def get(self):
		imagePost = db.get(self.request.get("img_id"))
		if imagePost.image:
			self.response.headers['Content-Type'] = "image/png"
			self.response.out.write(imagePost.image)
		else:
			self.error(404)
			
class ThumbnailRender (webapp.RequestHandler):
	def get(self):
		imagePost = db.get(self.request.get("img_id"))
		if imagePost.thumbnail:
			self.response.headers['Content-Type'] = "image/png"
			self.response.out.write(imagePost.thumbnail)
		else:
			self.error(404)

class PostImage(webapp.RequestHandler):
	def post(self):
		
		post = common.ImagePost()

		image = self.request.get("img")
		thumbnail = images.resize(image,100)
		middlesize = images.resize(image,200)
		
		post_id = int(self.request.get("post_id"))
	
		image_id = findImageIdNumber(post_id)
		
		image = self.request.get("img")
		    

		if(image):
			post.post_id = post_id
			post.image_id = image_id
			post.image = db.Blob(image)
			post.thumbnail = db.Blob(thumbnail)
			post.middlesize = db.Blob(middlesize)
			post.put()
		self.redirect('/edit?post=%d' % post_id)


class SortImage(webapp.RequestHandler):
	def get(self,post,curr,prev,next):
		post_id = int(post)
		curr_id = int(curr)
		prev_id = int(prev)
		next_id = int(next)

		


		if(next_id >= 0 and prev_id >= 0): #assuming that we're not pushing it at the last, and not putting it in front of all others
			self.response.out.write("assuming that we're not pushing it at the last, and not putting it in front of all others")
			if(curr_id < prev_id):
				self.response.out.write("lower things between curr and prev (inclusive of prev), replace prev with curr")
				imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id DESC",post_id)
				i = 0
				numToReplace = 0
				for ip in imagePosts:
					if(ip.image_id < next_id and ip.image_id >= curr_id ):
						if(i == 0):
							numToReplace = ip.image_id
						if(ip.image_id == curr_id):
							ip.image_id = numToReplace
							ip.put()
						else:
							ip.image_id = ip.image_id - 1
							ip.put()
						i += 1
			if(curr_id > next_id):
				self.response.out.write("raise things between next and curr (inclusive of next), replace next with curr")
				imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id ASC",post_id)
				i = 0
				numToReplace = 0
				for ip in imagePosts:
					if(ip.image_id >= next_id and ip.image_id <= curr_id ):
						if(i == 0):
							numToReplace = ip.image_id
						if(ip.image_id == curr_id):
							ip.image_id = numToReplace
							ip.put()
						else:
							ip.image_id = ip.image_id + 1
							ip.put()
						i += 1
					
		elif(next_id >= 0):  # only a next, meaning that we're inserting at the beginning
			self.response.out.write("only a next, meaning that we're inserting at the beginning")
			imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id ASC",post_id)
			i = 0
			for ip in imagePosts:
				if(ip.image_id == curr_id):
					ip.image_id = -1
					ip.put()
				if(ip.image_id >= next_id and ip.image_id < curr_id):
					ip.image_id = ip.image_id + 1
					ip.put()
				i += 1
			for ip in imagePosts:
				if(ip.image_id == -1):
					ip.image_id = 0
					ip.put()
			
					
		elif(prev_id >= 0): # only a previous, indicating that we're inserting at the end
			self.response.out.write("only a previous, indicating that we're inserting at the end")
			imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id DESC",post_id)
			i = 0
			highest = -1
			for ip in imagePosts:
				if(ip.image_id > highest):
					highest = ip.image_id
				if(ip.image_id == curr_id):
					ip.image_id = -1
					ip.put()
				if(ip.image_id <= prev_id and ip.image_id > curr_id):
					ip.image_id = ip.image_id - 1
					ip.put()
				i += 1
			for ip in imagePosts:
				if(ip.image_id == -1):
					ip.image_id = highest
					ip.put()		
					
class UpdatedImages(webapp.RequestHandler):
	def get(self,post):
		post_id = int(post)
		imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id ASC",post_id)
		for imagePost in imagePosts:
			self.response.out.write("<img id=\"%d\" src=\"/thumbnail?img_id=%s\"/>" %  (imagePost.image_id,imagePost.key()))
			
class ImageURLs(webapp.RequestHandler):
	def get(self,post):
		post_id = int(post)
		imageURLCode = common.getImageURLs(post_id)
		self.response.out.write(imageURLCode)
		
class PhonePost(webapp.RequestHandler):
	def post(self):
		post = common.ImagePost()
		image = self.request.get("img")
		thumbnail = images.resize(image,100)
		middlesize = images.resize(image,200)
		post_id = -1
		posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY post_id DESC LIMIT 1")
		for po in posts:
			post_id = po.post_id + 1
		image_id = findImageIdNumber(post_id)
		image = self.request.get("img")
		if(image):
			post.post_id = post_id
			post.image_id = image_id
			post.image = db.Blob(image)
			post.thumbnail = db.Blob(thumbnail)
			post.middlesize = db.Blob(middlesize)
			post.put()
			
			blogpost = common.BlogPost()
			blogpost.post_id = post_id
			
			titleFromPost = self.request.get("title")
			if(titleFromPost):
				blogpost.title = titleFromPost
			else:
				blogpost.title = "mobile picture"
			
			blogpost.content = "<br/><img src=\"/fullimage?img_id=%s\">" % post.key()
			if(str(self.request.get("published"))  == "Yes"  ):
				blogpost.published = True
			else:
				blogpost.published = False
			blogpost.put()

		
		
		
def main():
	application = webapp.WSGIApplication([('/img', Image),
										('/fullimage',FullImageRender),
										('/thumbnail',ThumbnailRender),
										(r'/updatedimages/(.*)',UpdatedImages),
										(r'/imageurls/(.*)',ImageURLs),
										('/phonepost',PhonePost),
										('/postimage',PostImage),
										(r'/sortimage/(.*)/(.*)/(.*)/(.*)',SortImage)
										],debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
