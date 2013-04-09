from milestone.models import Course, Question, Response
from django.utils import timezone

def new_course(name, term, yr):
	c = Course(course_name=name, course_term=term, year=yr)
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