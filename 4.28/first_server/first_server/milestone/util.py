from milestone.models import Course, Question, Response, Student_Question, Result
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

def new_student_question(c_id, netid, text, anon):
	c = Course.objects.get(pk=c_id)
	#flag = (anon == 'true')
	print 'made new student question: ', text, ' by ', netid
	c.student_question_set.create(question_text=text, user=netid, anonymous=anon, pub_date=timezone.now())

def add_upvote(c_id, sq_id):
	c = Course.objects.get(pk=c_id)
	q = c.student_question_set.get(pk=sq_id)
	q.upvotes += 1
	q.save()

def set_star(c_id, sq_id, status):
	c = Course.objects.get(pk=c_id)
	q = c.student_question_set.get(pk=sq_id)
	flag = (status == 'True')
	print flag, status
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
	r = q.response_set.filter(c_id=c_id, q_id=q_id, user=netid)
	#print r
	if r.count() != 0:
		r[0].delete();
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

def get_result(c_id, q_id):
	c = Course.objects.get(pk=c_id)
	q = c.question_set.get(pk=q_id)
	erase = Result.objects.filter(c_id=c_id).filter(q_id=q_id)
	for e in erase:
		e.delete()
	resps = Response.objects.filter(c_id=c_id).filter(q_id=q_id)
	for r in resps:
		check = Result.objects.filter(c_id=c_id).filter(q_id=q_id).filter(resp_text=r.resp_text)
		if not check:
			q.result_set.create(c_id=c_id, resp_text=r.resp_text, count=1)
		else:
			result = Result.objects.get(c_id=c_id, q_id=q_id, resp_text=r.resp_text)
			result.count += 1
			result.save()
	return Result.objects.filter(c_id=c_id).filter(q_id=q_id)


