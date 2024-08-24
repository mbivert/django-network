from django.shortcuts               import render, redirect
from django.contrib.auth            import login
from .forms                         import SigninForm, PostForm
from django.conf                    import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.views                   import generic
from .models                        import Post

def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)

			# Mimic LoginView's logic
			page = settings.LOGIN_REDIRECT_URL
			if request.POST['next']:
				page = request.POST['next']
			return redirect(page)

	return render(request, "network/signin.html", context={'form' : form})

@login_required(login_url='network:login')
def signout(request):
	if request.method == 'POST':
		request.user.delete()
		return redirect(settings.LOGOUT_REDIRECT_URL)

	return render(request, "network/signout.html")

class HomeView(generic.ListView):
	template_name       = "network/posts.html"
	context_object_name = "params"

	@method_decorator(login_required)
	def post(self, request):
		form = PostForm(request.POST)
		if form.is_valid():
			# ...
			post = form.save(commit=False)
			post.owner = request.user
			post.save()

		return render(request, self.template_name, context={
			"params" : {
				"form"  : form,
				"posts" : self.get_posts(),
			}
		})

	def get_posts(self):
		return Post.objects.order_by("-cdate")

	def get_queryset(self):
		return {
			"form"  : PostForm(initial={'next' : self.request.path}, auto_id=False),
			"posts" : self.get_posts(),
		}
