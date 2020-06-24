import hashlib

from django.core.cache import cache
from django.db.models import signals

import bbking.errors
import bbking.tags

class BBCodeField(object):
    def __init__(self, text_field='body', hash_field=None):
        self.text_field = text_field
        self.hash_field = hash_field

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls

        if self.hash_field:
            signals.pre_save.connect(self.update_hash_field, sender=cls)

        setattr(cls, name, self)

    def __get__(self, obj, instance_type = None):
        if obj is None:
            return self

        compiled_name = '_%s_compiled' % self.name
        try:
            return getattr(obj, compiled_name)
        except AttributeError:
            pass

        raw = getattr(obj, self.text_field)

        if self.hash_field:
            hash_key = getattr(obj, self.hash_field)
            if hash_key:
                compiled = cache.get('bbking:%s' % hash_key)
            else:
                compiled = bbking.tags.LiteralTag(raw)
        else:
            hash_key = None
            compiled = None

        if not compiled:
            try:
                compiled = bbking.tags.compile(raw)
            except bbking.errors.CompilationError:
                compiled = bbking.tags.LiteralTag(raw)

            if hash_key:
                cache.set('bbking:%s' % hash_key, compiled)

        setattr(obj, compiled_name, compiled)

        return compiled

    def update_hash_field(self, signal, sender, instance=None, **kwargs):
        raw = getattr(instance, self.text_field)

        try:
            compiled = bbking.tags.compile(raw)
        except bbking.errors.CompilationError:
            compiled = bbking.tags.LiteralTag(raw)

        if isinstance(compiled, bbking.tags.LiteralTag):
            hash_key = ''
        else:
            hash_key = hashlib.sha1(raw.encode('utf-8')).hexdigest()

        setattr(instance, self.hash_field, hash_key)

