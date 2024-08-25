from django.contrib.auth       import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models                   import Post
from django.forms              import ModelForm, Textarea

class SigninForm(UserCreationForm):
	template_name = "network/form_signin.html"
	class Meta(UserCreationForm.Meta):
		model  = get_user_model()
		fields = ['username', 'email']

class PostForm(ModelForm):
	template_name = "network/form_post.html"
	class Meta:
		model   = Post
		fields  = ['name', 'content']
		widgets = {
			"content": Textarea(attrs={"class": "content"}),
		}

class LoginForm(AuthenticationForm):
	template_name = "network/form_login.html"
	class Meta:
		model   = get_user_model()
		fields  = ['username', 'password']
		widgets = {
			"content": Textarea(attrs={"class": "content"}),
		}
