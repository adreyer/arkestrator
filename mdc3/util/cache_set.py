import datetime
import time

from django.core.cache import cache

class TimedCacheSet(object):
    def __init__(self, base_key, resolution = 60):
        self.base_key = base_key
        self.resolution = resolution

        #this may not work for times close to the epoch
        ts = int(time.mktime(datetime.datetime.now().timetuple()))
        self.curr = ts - (ts % resolution)
        self.prev = self.curr - resolution

    @property
    def curr_key(self):
        return "%s:%d" % (self.base_key, self.curr)

    @property
    def prev_key(self):
        return "%s:%d" % (self.base_key, self.prev)

    @property
    def full_set(self):
        curr_set = cache.get(self.curr_key, set())
        prev_set = cache.get(self.prev_key, set())
        return curr_set | prev_set

    def add_to_set(self, value):
        s = cache.get(self.curr_key, set())
        if value not in s:
            s |= set([value])
            cache.set(self.curr_key, s, 2 * self.resolution)
