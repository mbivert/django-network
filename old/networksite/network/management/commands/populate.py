from django.core.management.base import BaseCommand, CommandError

from network.utils import maybecreateuser, maybecreatepost

# This is a "dumb" command to populate the database with some data for
# tests.

class Command(BaseCommand):
	def handle(self, *args, **options):
		mb     = maybecreateuser("mb",     "m@b.com",     "mbmbmbmbmb")
		santa  = maybecreateuser("santa",  "san@ta.com",  "santasanta")
		djengo = maybecreateuser("djengo", "dje@ngo.com", "djengowwww")

		mb.follows.add(santa)
		mb.follows.add(djengo)
		djengo.follows.add(mb)

		mb.save()
		djengo.save()

		p0 = maybecreatepost("name0", mb,    "some random text")
		p1 = maybecreatepost("name1", santa, "more random text")
		print(p0.likers.all())
		p0.likers.add(mb)
		mb.likes.add(p0)
		print(p0.likers.all())
		print(mb.likes.all())
