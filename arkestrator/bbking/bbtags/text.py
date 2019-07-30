
from bbking.tags import BBTag

__all__ = ['BBTagItalic', 'BBTagBold', 'BBTagUnderline', 'BBTagStrikethrough']

class BBTagItalic(BBTag):
    tag_name = 'i'

class BBTagBold(BBTag):
    tag_name = 'b'

class BBTagUnderline(BBTag):
    tag_name = "u"

class BBTagStrikethrough(BBTag):
    tag_name = "strike"

