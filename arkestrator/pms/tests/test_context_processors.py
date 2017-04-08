from unittest2 import TestCase
from mock import Mock

from django.contrib.auth.models import User
from django.utils.unittest import TestCase as DJTestCase
from arkestrator.pms.models import PM, Recipient
from arkestrator.pms.context_processors import new_pm

class TestNewPM(TestCase):
    def test_anon(self):
        req = Mock()
        req.user.is_authenticated = lambda : False
        npm = new_pm(req)
        assert(npm == { 'new_pms' : 0})


class DJtests(DJTestCase):

    def test_one(self):
        user = User.objects.create(username='me')
        request = Mock()
        request.user = user
        pm = PM.objects.create(subject = 'test', sender=user)
        rec = Recipient.objects.create(message=pm, recipient=user)
        self.assertEqual(new_pm(request)['new_pms'], 1)
        rec.read = True
        rec.save()
        self.assertEqual(new_pm(request)['new_pms'], 0)
