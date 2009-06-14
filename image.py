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
		
		post_id = int(self.request.get("post_id"))
	
		image_id = findImageIdNumber(post_id)
		
		image = self.request.get("img")
		    

		if(image):
			post.post_id = post_id
			post.image_id = image_id
			post.image = db.Blob(image)
			post.thumbnail = db.Blob(thumbnail)
			post.put()
		self.redirect('/edit?post=%d' % post_id)

			
def main():
	application = webapp.WSGIApplication([('/img', Image),('/fullimage',FullImageRender),('/thumbnail',ThumbnailRender),('/postimage',PostImage)],debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
  main()
