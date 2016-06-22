from django.db import models
from django.contrib.auth.models import User

class ReportDatabase(models.Model):
	ITERM_TYPE = (
		('R', 'RNA-Seq with reference'),
		('D', 'RNA-Seq without reference'),
		('M', 'microRNA'),
		('C', 'Chip-Seq'),
	)
	ITERM_STATUS = (
		('U', 'Under way'),
		('P', 'Postpone'),
		('F', 'Finshed')
	)
	
	username = models.OneToOneField(User)
	userpwd = models.CharField(max_length=20, verbose_name='password')
	iterm_number = models.CharField(max_length=20, verbose_name='number', unique=True)
	iterm_report_name = models.CharField(max_length=30, verbose_name='report')
	iterm_path = models.CharField(max_length=100, verbose_name='path')
	iterm_type = models.CharField(max_length=1, verbose_name='type', choices=ITERM_TYPE)
	iterm_stime = models.DateTimeField()
	iterm_ftime = models.DateTimeField()
	iterm_status = models.CharField(max_length=1, verbose_name='status', choices=ITERM_STATUS)
	iterm_memo = models.TextField()

	def __unicode__(self):
		return unicode(self.username)

	class Meta:
		verbose_name = 'Report'
		verbose_name_plural = verbose_name

