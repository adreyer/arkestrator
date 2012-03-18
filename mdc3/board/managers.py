from django.db.managers import Manager

# Circular imports
from mdc3.board.models import LastRead, Favorites

class ThreadManager(Manager):
    def last_reads(self, user):
        """ Annotate a queryset of threads with the last read status for a user.
            Add an unread booleand to each thread
            if it was read before add a last_post_read id
            :note: WARNING: while this returns a queryset evaluating it again
                    will wipe out this information
            :TODO: make this hook into the evaluation.

            :params: user the user who should be looked up.
        """

        last_read = LastRead.objects.filter(
                thread__in=self,
                user = user).values('thread__id', 'post__id')
        last_viewed = dict((lr['thread__id'], lr) for lr in last_read)
        for t in self:
            try:
                # TODO: this will make a query for each thread
                t.unread = last_viewed[t.id]['post__id'] < t.last_post_id
                t.last_post_read = last_viewed[t.id]['post__id']
            except KeyError:
                t.unread = True

        return self

    def favorites(self, user):
        """ annotate a queryset of threads with a users favorites """
        favs = set(Favorites.objects.filter(
                                thread__in=self,
                                user=user).values('thread__id'))

        for thread in self:
            thread.fav = thread.id in favs
        return self
