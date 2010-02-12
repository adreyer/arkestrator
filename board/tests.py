from django.test import TestCase
from models import Thread, Post

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class ThreadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('foo','foo@bar.net','badpassword')
        self.site = Site.objects.get_current()

    def test_create_thread(self): 
        thread = Thread.on_site.create(
            subject="Hello, World",
            creator=self.user,
            last_post_by=self.user,
            site=self.site)

    def test_str(self):
        thread = Thread.on_site.create(
            subject="Hello, World",
            creator=self.user,
            last_post_by=self.user,
            site=self.site)

        self.assertEquals(thread.subject,"Hello, World")

