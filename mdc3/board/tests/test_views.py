from unittest2 import TestCase

import mock

from mdc3.board.views import ThreadList

class TestThreadList(TestCase):

    @mock.patch('mdc3.board.views.LastRead')
    def test_lrs(self, LR):
        """ make sure last reads are annotated correctly """
        vals = []
        for i in [1,2,4]:
            val = dict(thread__id=i, post__id=i*3)
            vals.append(val)
        qs = mock.Mock()
        qs.values.return_value = vals
        LR.objects.filter.return_value = qs
        thread_list = []
        last_posts = [[1,1],[2,4],[4,16],[5,25]]
        for i, j in last_posts:
            x = mock.Mock()
            x.id = i
            x.last_post_id = j
            thread_list.append(x)

        new_tl = ThreadList().last_reads(thread_list, "user1")
        for thread in new_tl:
            self.assertTrue(thread.id in [x[0] for x in last_posts])
            self.assertEqual(thread.unread, thread.id > 3)

    @mock.patch('mdc3.board.views.Favorite')
    def test_favs(self, fav):
        """ make sure favorites are annotated correctly """
        qs = mock.Mock()
        qs.values.return_value = [1,3,4,6]
        fav.objects.filter.return_value = qs
        thread_list = []
        for i in range(4):
            x = mock.Mock()
            x.id = i
            thread_list.append(x)

        new_tl = ThreadList().favorites(thread_list, "user1")
        for thread in new_tl:
            self.assertTrue(thread.id in range(4))
            self.assertEqual(thread.fav, thread.id in qs.values())
