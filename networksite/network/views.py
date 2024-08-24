from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth            import login
from .forms                         import SigninForm, PostForm
from django.conf                    import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.views                   import generic
from django.http                    import JsonResponse, HttpResponseRedirect
from .models                        import Post
from .utils                         import trydeletepost
from django.utils                   import timezone

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

	def newpost(self, request):
		form = PostForm(request.POST)
		if form.is_valid():
			# ...
			post = form.save(commit=False)
			post.owner = request.user
			post.save()
			return HttpResponseRedirect(request.POST['next'])

		return render(request, self.template_name, context={
			"params" : {
				"form"  : form,
				"posts" : self.get_posts(),
			}
		})

	@method_decorator(login_required(login_url='network:login'))
	def post(self, request):
		return self.newpost(request)

	def get_posts(self):
		return Post.objects.order_by("-cdate")

	def get_queryset(self):
		return {
			"form"  : PostForm(initial={'next' : self.request.path}, auto_id=False),
			"posts" : self.get_posts(),
		}

@login_required(login_url='network:login')
def delete(request, pk):
	p  = get_object_or_404(Post, pk=pk)

	err = ""
	msg = ""

	if trydeletepost(pk, request.user.id):
		msg = "deleted!"
	else:
		err = "( ͡° ͜ʖ ͡°)"

	if request.method == 'POST':
		return JsonResponse({'msg' : msg, 'err' : err})

	# Reasonable default (JS disabled)
	# TODO: add err/msg as GET parameter & process (also, untested)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='network:login')
def edit(request, pk):
	if request.method == 'POST':
		print(request, request.POST)
		p         = get_object_or_404(Post, pk=pk)
		p.content = request.body.decode('utf-8')
		p.mdate   = timezone.now()
		p.save()

	# XXX, now this one is really broken if there's no JS; we could
	# redirect to a special edition page & wire things properly.
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
