
from bbking import BBTag

__all__ = ['BBQuote']

class BBQuote(BBTag):
    tag_name = 'quote'


    def update_context(self, context):
        if self.arg:
            context['cite'] = self.arg

