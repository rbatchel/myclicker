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
	return HttpResponseRedirect('/login')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login')
	else:
		form = UserCreationForm()
	c = {'form': form}
	c.update(csrf(request))
	return render_to_response('registration/register.html', c)

@login_required	
def userhome(request):
	return render_to_response('userhome.html', {'user': request.user})


def start(request):
	return render_to_response('start.html')


@login_required
def update_xml(request):
	print "update_xml called"
	#for field in request.META:
	#	print field
	if request.is_ajax():
		#print "ajax method found"
		if request.method == 'GET':
			#print "ajax method called"
			#handle AJAX request here
			#parse input commands

			inputParam = request.GET
			c_id = inputParam.get('c_id', '1')
			q_id = inputParam.get('q_id', '1')
			action = inputParam.get('action', '')
			args = []
			for i in range(1, len(inputParam)-3):
				args.append(inputParam.get('str'+str(i), ''))
			user = request.user
			
			if action == 'sub_course':
				util.new_course(args[0], args[1], args[2], user)
			if action == 'sub_quest':
				util.new_question(c_id, args[0])
			if action == 'sub_resp':
				util.new_response(c_id, q_id, user.username, args[0])

			#args[0] is question text, args[1] is true/false for anonymous
			if action == 'sub_student_quest':
				util.new_student_question(c_id, user.username, args[0], args[1])
			#args[0] for upvote, args[1] for star and answered is student question id
			if action == 'upvote':
				util.add_upvote(c_id, args[0])
			if action == 'star':
				util.set_star(c_id, args[1], args[0])
			if action == 'answered':
				util.set_answered(c_id, args[1], args[0])
			if action == 'reset':
				util.clear_all()
			if action == 'set_open':
				print "set open", c_id, q_id, args[0]
				util.set_open(c_id, q_id, args[0])
			if action == 'set_hidden':
				print "set hidden", c_id, q_id, args[0]
				util.set_hidden(c_id, q_id, args[0])
			if action == 'edit_course':
				util.edit_course(c_id, args[0], args[1], args[2])
			if action == 'enroll':
				util.enroll_student(args[0], user)
			if action == 'unenroll':
				util.unenroll_student(c_id, user)
			if action == 'make_prof':
				util.make_prof(c_id, args[0])
			if action == 'remove_prof':
				util.remove_prof(c_id, args[0])


			
			data = serializers.serialize('xml', models.Response.objects.filter(c_id=c_id).filter(q_id=q_id))
			
			if action == 'get_course':
				data = serializers.serialize('xml', models.Course.objects.filter(pk=c_id))
			if (action == 'get_question' or action == 'set_open' or action == 'set_hidden'):
				data = serializers.serialize('xml', models.Question.objects.filter(c_id=c_id).filter(pk=q_id))
			if action == 'all_questions':
				data = serializers.serialize('xml', models.Question.objects.filter(c_id=c_id))
			if action == 'search':
				strs = args[0].split()
				searched = models.Course.objects.none()
				for s in strs:
					search_name = models.Course.objects.filter(course_name__contains=s)
					search_term = models.Course.objects.filter(course_term__contains=s)
					search_year = models.Course.objects.none()
					if s.isdigit():
						search_year = models.Course.objects.filter(year=int(s))
					searched = searched | search_name | search_term | search_year
				data = serializers.serialize('xml', searched)
			if action == 'search_duplicate':
				searched = models.Course.objects.filter(course_name__contains=args[0], course_term=args[1], year=int(args[2]))
				data = serializers.serialize('xml', searched)
			if action == 'search_duplicate_edit':
				searched = models.Course.objects.filter(course_name__contains=args[0], course_term=args[1], year=int(args[2]))
				data = serializers.serialize('xml', searched)
			if action == 'user_get_course_p':
				groups = user.groups.all()
				courses = models.Course.objects.none();
				for g in groups:
					if g.id % 2 == 0:
						courses = courses | models.Course.objects.filter(professors=g)
				data = serializers.serialize('xml', courses)
			if action == 'user_get_course_s':
				groups = user.groups.all()
				courses = models.Course.objects.none();
				for g in groups:
					if g.id % 2 == 1:
						courses = courses | models.Course.objects.filter(students=g)
				data = serializers.serialize('xml', courses)

			if action == 'student_questions':
				info = models.Student_Question.objects.filter(c_id=c_id).order_by('-pub_date')
				data = serializers.serialize('xml', info)
			print action
			if (action == 'get_results' or action == 'fill_chart'):
				print 'get_results called'
				data = serializers.serialize('xml', util.get_result(c_id, q_id))

		#	print data
			return HttpResponse(data, content_type='application/xml')

	#need to replace this file
	fp = open('./milestone/templates/milestone.html')
	t = template.Template(fp.read())
	fp.close()
	c = template.Context()
	html = t.render(c)
	return HttpResponse(html)


@login_required
def redirect(request, course, term, year):	
	print "redirect called"
	#values = course.split("#")
	#print values
	#name = values[0]
	name = course.replace("_", " ")
	print name, term, year
	year = int(year)
	data = models.Course.objects.filter(course_name__contains=name)
	#search through data to find the right term and year
	print data[0].id
	response = "you want course: " + name + "id = "
	id = -1
	for c in data:
		print c.course_term
		if c.course_term == term:
			print c.year
			if c.year == year:
				id = c.id
				print id
	#id = data[0].id 
	response = response + str(id)
	user = request.user
	groups = user.groups.all()
	print data[0].students
	print data[0].professors
	print user.groups.all()
	#name.replace(" ", " ")
	prof_name = name + "_P"
	student_name = name + "_S"
	for g in groups:
		search_name = g.name.replace("%20", " ")
		print len(search_name)
		if search_name == prof_name:
			return render_to_response('professor_id.html', {'user': request.user, 'c_id': id, 'classname': name})
			response = response + " and you're a professor"
		if search_name == student_name:
			return render_to_response('student_id.html', {'user': request.user, 'c_id': id, 'classname': name})
			response = response + " and you're a student"
	return HttpResponse("The class you are searching for has not been found.  Please ask our monkeys to examine your problem")

@login_required
def statistics(request, course, term, year):
	print "statistics called"
	name = course.replace("_", " ")
	data = models.Course.objects.filter(course_name__contains=name)
	year = int(year)
	id = -1
	for c in data:
		print c.students
		if c.course_term == term:
			print c.year
			if c.year == year:
				id = c.id
				print id
				#util.class_students(id)
	user = request.user
	groups = user.groups.all()
	prof_name = name + "_P"
	for g in groups:
		search_name = g.name.replace("%20", " ")
		if search_name == prof_name:
			#all student names are loaded as context
			list = ""
			c = models.Course.objects.get(pk=id)
			students = c.students
			print students.user_set.all()
			for s in students.user_set.all():
				print s
				list = list + str(s) + ' '
			print list
			#find total class questions: makes more sense to load them here
			questions = models.Question.objects.filter(c_id=id)
			print len(questions)
			return render_to_response('studentStatistics.html', {'user': request.user, 'c_id': id, 'classname': name, 'students': list, 'q_number': len(questions)})
	return HttpResponse("This page cannot be loaded.  Either you are looking for the wrong course, you don't have authorization, or you found a bug in our code.  Congratulations.")

 

@login_required
def info_xml(request):
	print "info_xml called"
	if request.is_ajax():
		if request.method == 'GET':
			#parse input commands
			inputParam = request.GET
			c_id = inputParam.get('c_id', '1')
			name = inputParam.get('user', '')
			action = inputParam.get('action', '')
			print action
			#action for all responses from a student
			if(action == 'student_responses'):
				set = models.Response.objects.filter(c_id=c_id).filter(user=name)
				data = serializers.serialize('xml', set)
				return HttpResponse(data, content_type='application/xml')
			if(action == 'class_questions'):
				set = models.Question.objects.filter(c_id=c_id)
				data = serializers.serialize('xml', set)
				return HttpResponse(data, content_type='application/xml')
			if(action == 'student_questions'):
				set = models.Student_Question.objects.filter(c_id=c_id, user=name).order_by('pub_date')
				data = serializers.serialize('xml', set)
				return HttpResponse(data, content_type='application/xml')

