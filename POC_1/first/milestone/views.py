# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django import template

#include model import and functions
from milestone import util, models
from django.core import serializers

def hello(request):
	return HttpResponse("Hello world")

def trial(request):
	fp = open('./milestone/templates/javascript.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def noxml(request):
	fp = open('./milestone/templates/noXML.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def xml(request):
	print "request called"
	#if request.method == 'POST':
	#	print "POST called"
	if request.is_ajax():
		print "is ajax"
		#handle AJAX request here
		#parse input commands
#		inputParam = request.POST
#		action = inputParam.get('action', '0')
#		str = inputParam.get('string', '0')
			#perform database requests
#		if action == 'update':
#			util.update(str)
#		if action == 'clear':
#			util.clear()
			#create xml
		output = serializers.serialize('xml', Record.objects.all())

			#send xml response
		return HttpResponse(output)

	#need to replace this file
	fp = open('./milestone/templates/milestone.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)



def update_xml(request):
	print "update_xml called"
	#for field in request.META:
	#	print field
	for object in request.GET:
		print object
	if request.is_ajax():
		print "ajax method found"
		if request.method == 'GET':
			print "ajax method called"
			#handle AJAX request here
			#parse input commands

			inputParam = request.GET
			action = inputParam.get('action', '0')
			str = inputParam.get('str', '0')
			print action
			print str

			if action == 'submit':
				util.update(str)
			if action == 'clear':
				util.clear()
			
			
			data = serializers.serialize('xml', models.Record.objects.all())
			print data
		#	output = data.getvalue()
		#	print output

			#send xml response
			print "returning an xml"
		
		#	return HttpResponse(data)	
			return HttpResponse(data, content_type='application/xml')

	#need to replace this file
	fp = open('./milestone/templates/milestone.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

#create url that only displays contents of database
def database(request):
	print "database request made"
	if request.is_ajax():
		print "ajax request made"
		data = serializers.serialize('xml', models.Record.objects.all())
		print data
		return HttpResponse(output)
	fp = open('./milestone/templates/withXML.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)
 

