import hashlib

from django.test import TestCase

from bbking import fields
from bbking.bbtags import text

class BBCodeFieldTestCase(TestCase):
    class FakeModel(object): #it's a faaaake
        bbcode = fields.BBCodeField(text_field = 'body')

        def __init__(self, body):
            self.body = body
            type(self).bbcode.contribute_to_class(type(self), 'bbcode')

    class FakeModelWithHash(FakeModel):
        bbcode = fields.BBCodeField(text_field = 'body', hash_field = 'hash')

        def __init__(self, body):
            self.body = body
            self.hash = None
            type(self).bbcode.contribute_to_class(type(self), 'bbcode')

        def save(self):
            type(self).bbcode.update_hash_field(None, type(self),self)

    def test_bbcode_field(self):
        fm = self.FakeModel(u"[i]\xa1This is a test![/i]")

        bbc = fm.bbcode
        self.assertEqual(type(bbc), text.BBTagItalic)

    def test_bbcode_with_hash(self):
        fm = self.FakeModelWithHash(u"[i]\xa1This is a test![/i]")

        fm.save()

        hashed = hashlib.sha1(u"[i]\xa1This is a test![/i]".encode('utf-8')).hexdigest()

        self.assertEqual(fm.hash, hashed)
    
    def test_no_hash_on_unparsed(self):
        fm = self.FakeModelWithHash(u"\xa1This is a test!")

        fm.save()

        self.assertEqual(fm.hash, '')
        
