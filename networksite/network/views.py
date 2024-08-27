from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth            import login
from .forms                         import SigninForm, PostForm
from django.conf                    import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.views                   import generic
from django.http                    import JsonResponse, HttpResponseRedirect, HttpResponse
from .models                        import Post, User
from .utils                         import trydeletepost, getfollowingposts
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
	paginate_by         = 5
	model               = Post

	def get_queryset(self):
		return Post.objects.order_by("-cdate")

	def get_context_data(self, **kwargs):
		context          = super().get_context_data(**kwargs)
		context['form']  = PostForm(auto_id=False)
		return context

	@method_decorator(login_required(login_url='network:login'))
	def post(self, request, *args, **kwargs):
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.owner = request.user
			post.save()
			# NOTE: if we POST, then we lose the HTTP GET parameters, in
			# particular the one used for pagination. POST['next'] still
			# contains it, so the redirection is safe.
			return HttpResponseRedirect(request.POST['next'])

		# This error case shouldn't impact a regular user, as
		# it requires handcrafted requests (HTML/JS would prevent).
		#
		# The current solution loses the error messages.
		#
		# Some of the solutions proposed here:
		#	https://docs.djangoproject.com/en/5.1/topics/class-based-views/mixins/#a-better-solution
		#
		# Feel dreadfully sophisticated. Storing the forms's error in
		# the request.session should be simpler, but perhaps somewhat
		# cumbersome.
#		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		return super().get(request, *args, **kwargs)
		# 'HomeView' object has no attribute 'object_list': we're missing
		# some wiring for get_context_data() to work, but could inject our
		# form in the context.
#		return render(request, self.template_name, context=self.get_context_data())

class FollowingView(HomeView):
	def get_queryset(self):
		return getfollowingposts(self.request.user)

class ProfileView(HomeView):
	is_profile = True

	# NOTE: this required a connected users; the only place where
	# this is called is guarded by a {% if user.is_authenticated %}
	def isfollow(self):
		return self.request.user.isfollow(self.kwargs["pk"])

	def get_user(self):
		return get_object_or_404(User, pk=self.kwargs["pk"])

	def get_queryset(self):
		return Post.objects.filter(owner=self.kwargs["pk"]).order_by("-cdate")

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

@login_required(login_url='network:login')
def like(request, pk):
	p  = get_object_or_404(Post, pk=pk)

	if p.likers.filter(pk=request.user.id):
		p.likers.remove(request.user)
	else:
		p.likers.add(request.user)

	if request.method == 'POST':
		return HttpResponse(p.nlikes)

	# Works without JS
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='network:login')
def follow(request, pk):
	u = get_object_or_404(User, pk=pk)

	# Can't follow oneself
	if request.user.pk != pk:
		action = "follow"
		if request.user.follows.filter(pk=u.id):
			request.user.follows.remove(u)
		else:
			request.user.follows.add(u)
			action = "unfollow"

		if request.method == 'POST':
			return JsonResponse({'action' : action, 'count' : u.nfollowers})

	# Works without JS
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))