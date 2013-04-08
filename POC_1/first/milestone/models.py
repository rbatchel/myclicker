from django.db import models

# Create your models here.

class Record(models.Model):
	str = models.CharField(max_length=200)
	def __unicode__(self):
		return self.str