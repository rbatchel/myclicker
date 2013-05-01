from django.db import models
from django.contrib.auth.models import Group

class Course(models.Model):
    students = models.ForeignKey(Group, related_name='students')
    professors = models.ForeignKey(Group, related_name='professors')
    course_name = models.CharField(max_length=7)
    course_term = models.CharField(max_length=6)
    year = models.IntegerField()

class Question(models.Model):
    c = models.ForeignKey(Course)
    question_text = models.CharField(max_length=200)
    is_open = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=True)
    pub_date = models.DateTimeField('date published')

class Student_Question(models.Model):
    c = models.ForeignKey(Course)
    question_text = models.CharField(max_length=200)
    user = models.CharField(max_length=10)
    upvotes = models.IntegerField(default=0)
    anonymous = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    
class Response(models.Model):
	q = models.ForeignKey(Question)
	c_id = models.IntegerField()
	user = models.CharField(max_length=10)
	resp_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

class Result(models.Model):
	q = models.ForeignKey(Question)
	c_id = models.IntegerField()
	resp_text = models.CharField(max_length=200)
	count = models.IntegerField()

