from django import forms

class PostForm(forms.Form):
	next    = forms.CharField(widget=forms.HiddenInput())
	# TODO: share maxlength with models.Post
	name    = forms.CharField(label="Name", max_length=120)
	content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "content"}))
