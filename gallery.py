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
		self.renderOutput = list()
		
	#
	#
	#	post_id = the post that the images in the gallery are associated with
	#   fromScratch = boolean variable - meaning are the jquery, jqueryui, lightbox, lightbox css invoked already or not
	#	forEditing = boolean variable - says whether it's being constructed for editing (sortable) or viewing (lightbox)
	#   
	def constructGallery(self,post_id,fromScratch,forEditing):
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
		""" % (post_id)
		if(fromScratch):
			self.renderOutput.append(javascriptCssInvoke)
		
		if(not forEditing): #assume it's for a gallery
			self.renderOutput.append(javascriptForGallery)
		else:
			self.renderOutput.append("""
					<script type="text/javascript">
						$(function() {
							$("#gallery_%d").sortable({
							   stop: function(event, ui) {
									//console.log(ui.item[0].previousElementSibling.id);
									//console.log(ui.item[0].nextElementSibling.id);
									//console.log(ui.item[0].id); //this is the item that was moved
									//console.log(ui.item[0].previousElementSibling);
									
									var prevElement;
									if( ui.item[0].previousElementSibling == null ){
										prevElement = -1;
									}else{
										prevElement = ui.item[0].previousElementSibling.id;
									}
									
									var nextElement;
									if( ui.item[0].nextElementSibling == null ){
										nextElement = -1;
									}else{
										nextElement = ui.item[0].nextElementSibling.id;
									}
									
									var thisElement = ui.item[0].id;

									
									
									
									if( prevElement == [null]){
										prevElement = -1;
									}
									if( nextElement == [null]){
										nextElement = -1;
									}
									
									$.ajax({
									  type: "GET",
									  url: "/sortimage/%d/" + thisElement + "/" + prevElement + "/" + nextElement ,
									  dataType: "script"
									});
									
									// this guy sends out a message of sortimages/postNumber/thisElement/previousElement/nextElement
									// previousElement or nextElement are -1 if they don't exist
									// to do: write a refresh into this specific div
									// something like this
									$("#gallery_%d").load("/updatedimages/%d");
								}
							});
							$("#gallery_%d").disableSelection();

						});

					</script>			
			""" % (post_id,post_id,post_id,post_id,post_id))
		self.renderOutput.append("<div id=\"gallery_%d\">\n" % post_id)
		imagePosts = db.GqlQuery("SELECT * FROM ImagePost WHERE post_id=:1 ORDER BY image_id ASC",post_id)
		for imagePost in imagePosts:
			if(forEditing):
				self.renderOutput.append("<img id=\"%d\" src=\"/thumbnail?img_id=%s\"/>" %  (imagePost.image_id,imagePost.key()))
			else:
				self.renderOutput.append("<a href=\"/fullimage?img_id=%s\" title=\"%s\"><img src=\"/thumbnail?img_id=%s\"/></a>" %  (imagePost.key(),imagePost.title,imagePost.key()))
				
		self.renderOutput.append("</div>\n")

	
	def gallerySpecificJsCss(self):
		return """
		<script type="text/javascript" src="/js/jquery.lightbox-0.5.min.js"></script>
		<link rel="stylesheet" type="text/css" href="/css/jquery.lightbox-0.5.css" media="screen" />
		"""
	def render(self):
		emptyString = ""
		for item in self.renderOutput:
			emptyString += item
		return emptyString