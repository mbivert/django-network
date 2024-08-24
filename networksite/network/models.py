from django.apps                    import apps
from django.contrib.auth.base_user  import BaseUserManager
from django.contrib.auth.hashers    import make_password
from django.contrib.auth.models     import UserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db                      import models
from django.utils                   import timezone
from django.utils.translation       import gettext_lazy as _
from django.conf                    import settings

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		if not username:
			raise ValueError("The given username must be set")
		email = self.normalize_email(email)
		# Lookup the real model class from the global app registry so this
		# manager method can be used in migrations. This is fine because
		# managers are by definition working on the real model.
		GlobalUserModel = apps.get_model(
			self.model._meta.app_label, self.model._meta.object_name
		)
		username = GlobalUserModel.normalize_username(username)
		user = self.model(username=username, email=email, **extra_fields)
		user.password = make_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email=None, password=None, **extra_fields):
		return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
	# password is the only field provided by AbstractBaseUser; we don't
	# need to specify it.

	username_validator = UnicodeUsernameValidator()

	username        = models.CharField(
		_("username"),
		max_length=150,
		unique=True,
		help_text=_(
			"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
		),
		validators=[username_validator],
		error_messages={
			"unique": _("A user with that username already exists."),
		},
	)
	email           = models.EmailField(_("email address"), blank=True)

	USERNAME_FIELD  = "username"
	EMAIL_FIELD     = "email"
	REQUIRED_FIELDS = ["email"]

	objects = UserManager()

	class Meta:
		verbose_name        = _("user")
		verbose_name_plural = _("users")

	# symmetrical=True (default), <=> systematic "follow-back"
	follows = models.ManyToManyField("self", symmetrical=False, related_name="followers")

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

	def save(self, *args, **kwargs):
		if not self.cdate:
			d = timezone.now()
			self.cdate = d
			self.mdate = d
		super().save(*args, **kwargs)