from bbking import BBTagWithArg

__all__ = ['BBTagHidden']

import string
import random
lnn = ''.join([string.ascii_letters, string.digits])

class BBTagHidden(BBTagWithArg):
    tag_name = 'hidden'

    def __init__(self, contents, arg='hidden'):
        super(BBTagHidden, self).__init__(contents,arg)

    def update_context(self, context):
        hiddenkey =''.join(random.choice(lnn) for i in range(10))
        context['hiddenkey'] = hiddenkey

    @classmethod
    def usage(cls):
        return[
            '[hidden=Button Text]stuff to be hidden[/hidden]',
            '[hidden]stuff to be hidden[/hidden]',
            ]
