from milestone.models import Course, Question, Response
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