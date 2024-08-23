from django.shortcuts import get_object_or_404
from django.views     import generic
from .models          import Post, User
from .forms           import PostForm
from django.http      import HttpResponseRedirect
from django.urls      import reverse
from django.utils     import timezone

class AllPostsView(generic.ListView):
	template_name       = "network/posts.html"
	context_object_name = "params"

	def get_queryset(self):
		return {
			"posts" : Post.objects.order_by("-cdate"),
			"form"  : PostForm(initial={'next' : self.request.path}, auto_id=False),
		}

class EditView(generic.edit.FormMixin, generic.DetailView):
	model = Post
	template_name = "network/edit.html"
	form_class = PostForm(initial={'next' : self.request.path}, auto_id=False)

	# TODO: factor with delete
	def post(self, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse("network:login"))

		# Could also have been a hidden field
		pk      = kwargs['pk']
		form = PostForm(self.request.POST)

		# next should be okay still?
		if not form.is_valid():
			print("form issue?")
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

		name    = form.cleaned_data.name
		content = form.cleaned_data.content
#		name    = self.request.POST["name"]
#		content = self.request.POST["content"]

		owner   = self.request.user

		p  = get_object_or_404(Post, pk=pk)

		if p.owner.id != owner.id:
			print("can't delete that!")
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

		p.name    = name
		p.content = content
		p.mdate   = timezone.now()
		p.save()
		return HttpResponseRedirect(reverse("network:allposts"))

class FollowingView(generic.ListView):
	template_name       = "network/posts.html"
	context_object_name = "posts"

	def get(self, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse("network:allposts"))
		return super(FollowingView, self).get(*args, **kwargs)

	# TODO: tests
	def get_queryset(self):
		uids = [ u.id for u in self.request.user.follows.all() ]
		print(uids)
		return Post.objects.filter(owner__in=uids).order_by("-cdate")

class ProfileView(generic.ListView):
	template_name       = "network/posts.html"
	context_object_name = "posts"

	def is_profile(self):
		return True

	def get_user(self):
		return get_object_or_404(User, pk=self.kwargs["pk"])

	def get_queryset(self):
		return Post.objects.filter(owner=self.kwargs["pk"]).order_by("-cdate")

# XXX Maybe there's a default view for those?
def addpost(request):
	name    = request.POST["name"]
	content = request.POST["content"]
	next    = request.POST["next"]
	owner   = request.user

	p = Post(name=name, owner=owner, content=content)
	p.save()
	return HttpResponseRedirect(next)

# TODO: redirection is kinda meh (broken if referer disabled by browser), error handling
def delete(request, pk):
	if not request.user.is_authenticated:
		print("not authenticated") # TODO
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

	p  = get_object_or_404(Post, pk=pk)

	if p.owner.id != request.user.id:
		print("can't delete that!")
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

	p.delete()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def like(request, pk):
	if not request.user.is_authenticated:
		print("not authenticated") # TODO
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

	p  = get_object_or_404(Post, pk=pk)

	if p.likers.filter(pk=request.user.id):
		p.likers.remove(request.user)
	else:
		p.likers.add(request.user)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def follow(request, pk):
	if not request.user.is_authenticated:
		print("not authenticated") # TODO
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

	u = get_object_or_404(User, pk=pk)

	if request.user.follows.filter(pk=u.id):
		request.user.follows.remove(u)
	else:
		request.user.follows.add(u)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
