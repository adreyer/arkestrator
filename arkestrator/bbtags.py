from .bbking.tags import BBTag

__all__ = ['BBTagHidden']

import string
import random
lnn = ''.join([string.ascii_letters, string.digits])

class BBTagHidden(BBTag):
    tag_name = 'hidden'
    default_arg = 'hidden'

    def update_context(self, context):
        hiddenkey =''.join(random.choice(lnn) for i in range(10))
        context['hiddenkey'] = hiddenkey

    @classmethod
    def usage(cls):
        return[
            '[hidden=Button Text]stuff to be hidden[/hidden]',
            '[hidden]stuff to be hidden[/hidden]',
            ]
