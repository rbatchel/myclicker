from milestone.models import Record

def update(s):
	r = Record(str = s)
	r.save()

def clear():
	for r in Record.objects.all():
		r.delete()