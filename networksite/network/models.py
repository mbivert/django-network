from django.db                  import models
from django.conf                import settings
from django.contrib.auth.models import AbstractUser
from django.utils               import timezone

class Post(models.Model):
	owner   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name    = models.CharField(max_length=120)
	content = models.TextField()

	# NOTE: if we use default=timezone.now, we'll get slightly two distinct
	# dates on post creation, which is not what we want; so we override
	# the blank in save() later
	cdate   = models.DateTimeField("creation date",     blank=True)
	mdate   = models.DateTimeField("modification date", blank=True)

	likers  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")

	@property
	def nlikes(self):
		return len(self.likers.all())

	def save(self, *args, **kwargs):
		if not self.cdate:
			d = timezone.now()
			self.cdate = d
			self.mdate = d
		super().save(*args, **kwargs)

class User(AbstractUser):
	# symmetrical=True (default), <=> systematic "follow-back"
	follows = models.ManyToManyField("self", symmetrical=False, related_name="followers")

	@property
	def nfollows(self):
		return len(self.follows.all())

	@property
	def nfollowers(self):
		return len(self.followers.all())
