from django.contrib.auth       import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models                   import Post
from django.forms              import ModelForm, Textarea

# TODO: use a template for that form
class SigninForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = get_user_model()
		fields = ['username', 'email']

class PostForm(ModelForm):
	template_name = "network/form_post.html"
	class Meta:
		model   = Post
		fields  = ['name', 'content']
		widgets = {
			"content": Textarea(attrs={"class": "content"}),
		}
