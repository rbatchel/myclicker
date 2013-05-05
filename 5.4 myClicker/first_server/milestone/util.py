from milestone import models
from milestone.models import Course, Question, Response, Student_Question, Result, User_Liked
from django.contrib.auth.models import User, Group
from django.utils import timezone

def new_course(name, term, year, user):
	Group.objects.get_or_create(name=name+'_S')
	students = Group.objects.get(name=name+'_S')
	Group.objects.get_or_create(name=name+'_P')
	professors = Group.objects.get(name=name+'_P')
	professors.user_set.add(user)
	professors.save()
	c = Course(course_name=name, course_term=term, year=year, students=students, professors=professors)
	#c = Course(course_name=name, course_term=term, year=yr, professors=professors)
	c.save()
	
def edit_course(c_id, name, term, year):
	c = Course.objects.get(pk=c_id)
	c.students.name = name+'_S'
	c.professors.name = name+'_P'
	c.students.save()
	c.professors.save()
	c.course_name = name
	c.course_term = term
	c.year = year
	c.save()
	
def new_question(c_id, text):
	c = Course.objects.get(pk=c_id)
	c.question_set.create(question_text=text, pub_date=timezone.now())

def new_student_question(c_id, netid, text):
	c = Course.objects.get(pk=c_id)
	#flag = (anon == 'true')
	print 'made new student question: ', text, ' by ', netid
	c.student_question_set.create(question_text=text, user=netid, pub_date=timezone.now())

def add_upvote(c_id, sq_id, netid):
	c = Course.objects.get(pk=c_id)
	q = c.student_question_set.get(pk=sq_id)
	u = models.User_Liked.objects.filter(s=q, user=netid)
	if u.count() == 0:
		q.user_liked_set.create(user=netid)
		q.upvotes += 1
		q.save()

def set_star(c_id, sq_id, status):
	c = Course.objects.get(pk=c_id)
	q = c.student_question_set.get(pk=sq_id)
	flag = (status == 'True')
	q.is_starred = flag
	q.save()

def set_answered(c_id, sq_id, status):
	c = Course.objects.get(pk=c_id)
	q = c.student_question_set.get(pk=sq_id)
	flag = (status == 'True')
	q.is_answered = flag
	q.save()
	
def set_open(c_id, q_id, status):
	c = Course.objects.get(pk=c_id)
	q = c.question_set.get(pk=q_id)
	flag = (status == 'True')
	q.is_open = flag
	q.save()
	
def set_hidden(c_id, q_id, status):
	c = Course.objects.get(pk=c_id)
	q = c.question_set.get(pk=q_id)
	flag = (status == 'True')
	q.is_hidden = flag
	q.save()
	
def new_response(c_id, q_id, netid, text):
	c = Course.objects.get(pk=c_id)
	q = c.question_set.get(pk=q_id)
	q.response_set.create(c_id=c_id, user=netid, resp_text=text, pub_date=timezone.now())
	
def enroll_student(c_id, user):
	c = Course.objects.get(pk=c_id)
	c.students.user_set.add(user)
	c.students.save()
	
def make_prof(c_id, username): #assumes user is a student
	user = User.objects.get(username=username)
	c = Course.objects.get(pk=c_id)
	c.students.user_set.remove(user)
	c.students.save()
	c.professors.user_set.add(user)
	c.professors.save()
	
def clear_courses():
	for c in Course.objects.all():
		c.delete()
		
def clear_questions():
	for q in Question.objects.all():
		q.delete()
				
def clear_responses():
	for r in Response.objects.all():
		r.delete()
		
def clear_all():
	clear_courses()
	clear_questions()
	clear_responses()

def enroll_student(c_id, user):
	c = Course.objects.get(pk=c_id)
	c.students.user_set.add(user)
	c.students.save()

def unenroll_student(c_id, user):
	print c_id, user
	c = Course.objects.get(pk=c_id)
	print c.course_name
	print user.username
	c.students.user_set.remove(user)
	c.students.save()

def make_prof(c_id, username): #assumes user is a student
	user = User.objects.get(username=username)
	c = Course.objects.get(pk=c_id)
	c.students.user_set.remove(user)
	c.students.save()
	c.professors.user_set.add(user)
	c.professors.save()

def remove_prof(c_id, username): #assumes user is a professor
	user = User.objects.get(username=username)
	c = Course.objects.get(pk=c_id)
	print username, c.course_name
	c.students.user_set.add(user)
	c.students.save()
	c.professors.user_set.remove(user)
	c.professors.save()
	
def get_resp(c_id, q_id):
	return models.Response.objects.filter(c_id=c_id).filter(q_id=q_id)

def get_course(c_id):
	return models.Course.objects.filter(pk=c_id)
	
def get_quest(c_id, q_id):
	return models.Question.objects.filter(c_id=c_id).filter(pk=q_id)

def all_quest(c_id):
	return models.Question.objects.filter(c_id=c_id)

def search(input):
	strs = input.split()
	check = models.Course.objects.none()
	searched = models.Course.objects.all()
	l = len(searched)
	for s in strs:
		search_name = models.Course.objects.filter(course_name__contains=s)
		search_term = models.Course.objects.filter(course_term__contains=s)
		search_year = models.Course.objects.none()
		if s.isdigit():
			search_year = models.Course.objects.filter(year=int(s))
		if search_name: searched = searched & search_name
		if search_term: searched = searched & search_term
		if search_year: searched = searched & search_year
		check = check | search_name | search_term | search_year
	if not check and len(searched) == l:
		return models.Course.objects.none()
	return searched
	
def get_course_p(user):
	groups = user.groups.filter(name__regex=r'P$')
	courses = models.Course.objects.none();
	for g in groups:
		courses = courses | models.Course.objects.filter(professors=g) 
	return courses
	
def get_course_s(user):
	groups = user.groups.filter(name__regex=r'S$')
	courses = models.Course.objects.none();
	for g in groups:
		courses = courses | models.Course.objects.filter(students=g) 
	return courses

def get_result(c_id, q_id):
	c = Course.objects.get(pk=c_id)
	q = c.question_set.get(pk=q_id)
	erase = models.Result.objects.filter(c_id=c_id).filter(q_id=q_id)
	for e in erase:
		e.delete()
	resps = models.Response.objects.filter(c_id=c_id).filter(q_id=q_id)
	for r in resps:
		check = models.Result.objects.filter(c_id=c_id).filter(q_id=q_id).filter(resp_text__iexact=r.resp_text)
		if not check:
			q.result_set.create(c_id=c_id, resp_text=r.resp_text, count=1)
		else:
			result = models.Result.objects.get(c_id=c_id, q_id=q_id, resp_text__iexact=r.resp_text)
			result.count += 1
			result.save()
	return models.Result.objects.filter(c_id=c_id).filter(q_id=q_id)

def get_userstatus(c_id, q_id, user):
	c = Course.objects.get(pk=c_id)
	s = c.students.user_set.all()
	p = c.professors.user_set.all()
	q = c.question_set.get(pk=q_id)
	professor, student_allow, student, other, all = range(5)
	user_status = other
	if user in p: 
		user_status = professor
	if user in s:
		if not q.is_hidden: 
			user_status = student_allow
		else:
			user_status = student
	return user_status