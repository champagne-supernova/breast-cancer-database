import re
from django import forms

#class ReportRegisterForm(forms.Form):
#	username = forms.RegexField(regex=r'^\w+$',
#								widget=forms.TextInput(attr=dict(required='True', max_length=30)),
#								)
#	password = forms.CharField(widget=forms.PasswordInput)

class BlastForm(forms.Form):
	query_sequence = forms.CharField(widget=forms.Textarea, label='Enter Query Sequence', required=False)
	def attribute_infos(self):
		self.fields['query_sequence'].widget.attrs={'rows': ROWS_NUMBER, 'cols': COLS_NUMBER}

