from .models              import User, Post

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
