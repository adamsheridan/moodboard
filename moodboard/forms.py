from django import forms
from moodboard.models import Image, Board, Comment
import urllib.request as urlr

class ImageForm(forms.ModelForm):

	def clean(self):
		'''
			Validate image URL
		'''
		try:
			image = urlr.urlopen(self.cleaned_data['url_external'])
			if image.code == 200:
				return self.cleaned_data
			else:
				raise forms.ValidationError('URL does not resolve')
		except: 
			raise forms.ValidationError('URL is not valid')

	class Meta:
		model = Image
		fields = ['name', 'url_external', 'board']

class BoardForm(forms.ModelForm):
	class Meta:
		model = Board
		fields = ['name', 'description']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'comment', 'image']