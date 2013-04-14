# Create your views here.

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import logout
from django.core import serializers
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from milestone import util, models
from django.core.context_processors import csrf

#include model import and functions

#===============================================================================
# def login(request):
# 	print "student request"
# 	fp = open('./milestone/templates/login.html')
# 	t = template.Template(fp.read())
# 	fp.close()
# 	c = template.Context()
# 	html = t.render(c)
# 	return HttpResponse(html)
#===============================================================================

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/milestone/login')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/milestone/login')
	else:
		form = UserCreationForm()
	c = {'form': form}
	c.update(csrf(request))
	return render_to_response('registration/register.html', c)

@login_required
def student(request):
	#===========================================================================
	# print "student request"
	# fp = open('./milestone/templates/student.html')
	# t = template.Template(fp.read())
	# fp.close()
	# c = template.Context()
	# html = t.render(c)
	# return HttpResponse(html)
	#===========================================================================
	return render_to_response('student.html', {'user': request.user})

def student_base(request):
	print file
	fp = open('./milestone/templates/stylesheets/base.css')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def student_layout(request):
	print file
	fp = open('./milestone/templates/stylesheets/layout.css')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def student_skeleton(request):
	print file
	fp = open('./milestone/templates/stylesheets/skeleton.css')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def professor(request):
	fp = open('./milestone/templates/professor.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def professor_base(request):
	print file
	fp = open('./milestone/templates/stylesheets/base.css')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	#print HttpResponse(html)
	return HttpResponse(html)

def professor_layout(request):
	print file
	fp = open('./milestone/templates/stylesheets/layout.css')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def professor_skeleton(request):
	print file
	fp = open('./milestone/templates/stylesheets/skeleton.css')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

def professor_icon(request):
	print file
	fp = open('./milestone/templates/images/favicon.ico')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)

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

@login_required
def update_xml(request):
	print "update_xml called"
	#for field in request.META:
	#	print field
	if request.is_ajax():
		print "ajax method found"
		if request.method == 'GET':
			print "ajax method called"
			#handle AJAX request here
			#parse input commands

			inputParam = request.GET
			c_id = inputParam.get('c_id', '')
			q_id = inputParam.get('q_id', '')
			action = inputParam.get('action', '')
			args = []
			for i in range(1, len(inputParam)-3):
				args.append(inputParam.get('str'+str(i), ''))
			user = request.user
				
			if action == 'sub_course':
				util.new_course(args[0], args[1], args[2])
			if action == 'sub_quest':
				util.new_question(c_id, args[0])
			if action == 'sub_resp':
				util.new_response(c_id, q_id, user.username, args[0])
			if action == 'reset':
				util.clear_all()
			if action == 'set_open':
				util.set_open(c_id, q_id, args[0])
			if action == 'set_hidden':
				util.set_hidden(c_id, q_id, args[0])
			
			data = serializers.serialize('xml', models.Response.objects.filter(c_id=c_id).filter(q_id=q_id))
			
			if action == 'get_course':
				data = serializers.serialize('xml', models.Course.objects.filter(pk=c_id))
			if (action == 'get_question' or action == 'set_open' or action == 'set_hidden'):
				data = serializers.serialize('xml', models.Question.objects.filter(c_id=c_id).filter(pk=q_id))
			if (action == 'all_questions'):
				data = serializers.serialize('xml', models.Question.objects.filter(c_id=c_id))

			print data
			
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
		data = serializers.serialize('xml', models.Response.objects.all())
		print data
		return HttpResponse(output)
	fp = open('./milestone/templates/withXML.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)
 

