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


class Hour(RandomWordFilter):
    open_pattern = re.compile('hour',re.IGNORECASE)
    word='dopesmoker'
    orig='hour'
    prob=.25

class Upgrade(RandomWordFilter):
    open_pattern = re.compile('upgrade',re.IGNORECASE)
    word='UPGRAYEDD'
    orig='upgrade'
    prob=.25
    
class Fuck(WordFilter):
    open_pattern = re.compile('fuck',re.IGNORECASE)
    word='fudge'

class Shit(WordFilter):
    open_pattern = re.compile('shit',re.IGNORECASE)
    word = 'shoot'


register(Upgrade)
register(Hour)
register(Shit)
register(Fuck)


