import re
import random
from bbcode import *


class WordFilter(SelfClosingTagNode):
    def parse(self):
        return self.word

class MultiWordFilter(SelfClosingTagNode):
    def parse(self):
        return random.choice(self.word_list)
    
class RandomWordFilter(SelfClosingTagNode):
    def parse(self):
        if random.random() < self.prob:
            return self.word
        else:
            return self.orig


class Hour(WordFilter):
    open_pattern = re.compile('hour',re.IGNORECASE)
    word='dopesmoker'

class Upgrade(WordFilter):
    open_pattern = re.compile('upgrade',re.IGNORECASE)
    word='UPGRAYEDD'

class Mee(WordFilter):
    open_pattern = re.compile(' mee ',re.IGNORECASE)
    word=' me '

register(Upgrade)
register(Hour)
register(Mee)



