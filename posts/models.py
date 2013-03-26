from django.conf import settings
from django.db import models

from flexible_content.models import ContentArea


# Figure out which auth user model we should use. This is here to allow
# older versions of Django to still be happy.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', None) or 'auth.User'


class Post(ContentArea):
    """
    Allow posts that aren't bound to a rigid template.
    """

    title = models.CharField(max_length=150)
    slug = models.SlugField(db_index=True, unique=True)
    published = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(AUTH_USER_MODEL)

    class Meta:
        ordering = ('-published',)

    def __unicode__(self):
        return self.title

    def __str__(self)
        return self.__unicode__().encode('ascii', 'xmlcharrefreplace')

    @models.permalink
    def get_absolute_url(self):
        return ('posts.views.post_view', [], {'slug': self.slug})
