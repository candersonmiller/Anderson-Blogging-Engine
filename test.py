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
import gallery



class Test(webapp.RequestHandler):
	def get(self):
		#self.response.headers['Content-Type'] = 'text/html'

		self.response.out.write(template.render('uploadtest.html',{'post_id' : 2}))
		#self.response.out.write("""
	     #   <html>
	     #    <body>
	     #       <form action="/postimage" enctype="multipart/form-data"  method="post">
		#	        <div>post_id: <textarea name="post_id" ></textarea></div>
		#	        <div><input type="file" name="img"/><</div>
		#			<div><input type="submit" value="Post To List"></div>
	     #       </form>
	      #    </body>
	      #  </html>""")
		#new_gallery = gallery.Gallery()
		#new_gallery.constructGallery(2,True)
		#self.response.out.write(new_gallery.render())
		#new_gallery = gallery.Gallery()
		#new_gallery.constructGallery(0,False)
		#self.response.out.write(new_gallery.render())

			

def main():
	application = webapp.WSGIApplication([('/test',Test)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()