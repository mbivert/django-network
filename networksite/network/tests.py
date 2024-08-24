# XPutall; Clear; python manage.py test -v 2 network
from django.test import TestCase

from .utils import maybecreateuser, maybecreatepost, getfollowsposts

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

class LikingTests(TestCase):
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

		likes = [ p.content for p in mb.likes.all().order_by("content") ]
		self.assertSequenceEqual(likes, [])

		p0.likers.add(mb)
		santa.likes.add(p0)
		mb.likes.add(p1)

		likers = [ u.username for u in p0.likers.all().order_by("username") ]
		self.assertSequenceEqual(likers, ["mb", "santa"])

		likes = [ p.content for p in mb.likes.all().order_by("content") ]
		self.assertSequenceEqual(likes, ["more random text", "some random text"])

		likers = [ u.username for u in p1.likers.all().order_by("username") ]
		self.assertSequenceEqual(likers, ["mb"])

		likes = [ p.content for p in santa.likes.all().order_by("content") ]
		self.assertSequenceEqual(likes, ["some random text"])

class GetFollowsPostsTests(TestCase):
	def test_getfollowsposts(self):
		"""
		Make sure we can retrieve posts from people we follow.
		"""
		mb     = maybecreateuser("mb",     "m@b.com",     "mbmbmbmbmb")
		santa  = maybecreateuser("santa",  "san@ta.com",  "santasanta")
		djengo = maybecreateuser("djengo", "dje@ngo.com", "djengowwww")

		p0 = maybecreatepost("name0", mb,    "some random text")
		p1 = maybecreatepost("name1", santa, "more random text")

		mb.follows.add(santa)
		mb.follows.add(djengo)
		djengo.follows.add(mb)

		# mb follows santa (1 post) djengo (0 posts)
		ps = [p.content for p in getfollowsposts(mb)]
		self.assertSequenceEqual(ps, ["more random text"])

		# djengo follows mb (1 post)
		ps = [p.content for p in getfollowsposts(djengo)]
		self.assertSequenceEqual(ps, ["some random text"])

		# santa follows no one
		ps = [p.content for p in getfollowsposts(santa)]
		self.assertSequenceEqual(ps, [])
