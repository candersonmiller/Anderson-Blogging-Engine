#!/usr/bin/env python
# encoding: utf-8
"""
gallery.py
 
Created by C. Anderson Miller on 2009-06-14.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.ext.webapp import template

import common


class Gallery():
 
	def main():
		print "oh hai!"

	def __init__(self):
		self.renderOutput = ""
		
	#
	#
	#	post_id = the post that the images in the gallery are associated with
	#   fromScratch = boolean variable - meaning are the jquery, jqueryui, lightbox, lightbox css invoked already or not
	#	
	def constructGallery(self,post_id,fromScratch):
		javascriptCssInvoke = """
			<script type="text/javascript" src="http://www.google.com/jsapi?key=ABQIAAAA-xDrjSBaHCs5B0t85D904xRq4LgvBueVH8RF3cRGkvic6WQ2NxQXZ_rzqp1XfgsrmFzFNIaWDHF5hQ"></script>
			<script type="text/javascript">
				google.load("jquery", "1.3.2");
				google.load("jqueryui", "1.7.2");
			</script> 
			<script type="text/javascript" src="/js/jquery.lightbox-0.5.min.js"></script>
			<link rel="stylesheet" type="text/css" href="/css/jquery.lightbox-0.5.css" media="screen" />
		"""
		javascriptForGallery = """
			<script type="text/javascript">
				$(function() {
					$('#gallery_%d a').lightBox({fixedNavigation:true});
				});
			</script>
		""" % post_id
		if(fromScratch):
			self.renderOutput += javascriptCssInvoke
		self.renderOutput += javascriptForGallery
		self.renderOutput += "<div id=\"gallery_%d\">\n" % post_id
		imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id ASC",post_id)
		for imagePost in imagePosts:
			self.renderOutput += "<a href=\"/fullimage?img_id=%s\" title=\"%s\"><img src=\"/thumbnail?img_id=%s\"/></a>" %  (imagePost.key(),imagePost.title,imagePost.key())
			#<a href="largeImage" title="ImageTitle"><img src="smallImage"/></a>
		self.renderOutput += "</div>\n"

	
	def gallerySpecificJsCss(self):
		return """
		<script type="text/javascript" src="/js/jquery.lightbox-0.5.min.js"></script>
		<link rel="stylesheet" type="text/css" href="/css/jquery.lightbox-0.5.css" media="screen" />
		"""
	def render(self):
		return self.renderOutput