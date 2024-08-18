# XPutall; Clear; python manage.py test -v 2 network
from django.test import TestCase

from .utils import maybecreateuser, maybecreatepost

class FollowingTests(TestCase):
	def test_following_users(self):
		"""
		Ensure the DB scheme to correctly implements the "follows" relationship.
		"""
		mb     = maybecreateuser("mb",     "m@b.com",     "mbmbmbmbmb")
		santa  = maybecreateuser("santa",  "san@ta.com",  "santasanta")
		djengo = maybecreateuser("djengo", "dje@ngo.com", "djengowwww")

		mb.follows.add(santa)
		mb.follows.add(djengo)
		djengo.follows.add(mb)

		mb.save()
		djengo.save()

		follows = [ u.username for u in mb.follows.all().order_by("username") ]
		# Works as well
#		follows = mb.follows.all().order_by("username").values_list("username", flat=True)
		self.assertSequenceEqual(follows, ["djengo", "santa"])

		follows = [ u.username for u in djengo.follows.all().order_by("username") ]
		self.assertSequenceEqual(follows, ["mb"])

		follows = [ u.username for u in santa.follows.all().order_by("username") ]
		self.assertSequenceEqual(follows, [])

	def test_likes_posts(self):
		"""
		Ensure the DB scheme correctly allows users to like posts.
		"""
		mb     = maybecreateuser("mb",     "m@b.com",     "mbmbmbmbmb")
		santa  = maybecreateuser("santa",  "san@ta.com",  "santasanta")
		djengo = maybecreateuser("djengo", "dje@ngo.com", "djengowwww")

		p0 = maybecreatepost("name0", mb,    "some random text")
		p1 = maybecreatepost("name1", santa, "more random text")

		likers = [ u.username for u in p0.likers.all().order_by("username") ]
		self.assertSequenceEqual(likers, [])

		likes = [ p.text for p in mb.likes.all().order_by("text") ]
		self.assertSequenceEqual(likes, [])

		p0.likers.add(mb)
		santa.likes.add(p0)
		mb.likes.add(p1)

		likers = [ u.username for u in p0.likers.all().order_by("username") ]
		self.assertSequenceEqual(likers, ["mb", "santa"])

		likes = [ p.text for p in mb.likes.all().order_by("text") ]
		self.assertSequenceEqual(likes, ["more random text", "some random text"])

		likers = [ u.username for u in p1.likers.all().order_by("username") ]
		self.assertSequenceEqual(likers, ["mb"])

		likes = [ p.text for p in santa.likes.all().order_by("text") ]
		self.assertSequenceEqual(likes, ["some random text"])
