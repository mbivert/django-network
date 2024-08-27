from .models              import User, Post
from django.shortcuts     import get_object_or_404

def maybecreateuser(username, email, password):
	try:
		u = User.objects.get(username=username)
	except User.DoesNotExist:
		u = User.objects.create_user(username, email, password)
		u.save()
	return u

def maybecreatepost(name, owner, content):
	try:
		p = Post.objects.get(name=name)
	except Post.DoesNotExist:
		p = Post(name=name, owner=owner, content=content)
		p.save()
	return p

def trydeletepost(pk, uid):
	p  = get_object_or_404(Post, pk=pk)
	if p.owner.id == uid:
		p.delete()
		return True
	return False

def getfollowingposts(user):
	uids = [ u.id for u in user.follows.all() ]
	return Post.objects.filter(owner__in=uids).order_by("-cdate")
