from django.conf import settings
from django.db import models
from django.utils.timezone import now as tz_now

from taggit.managers import TaggableManager
from flexible_content.models import ContentArea


# Figure out which auth user model we should use. This is here to allow
# older versions of Django to still be happy.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', None) or 'auth.User'


class PostManager(models.Manager):
    """
    Add quick endpoints for sets of posts.
    """

    def published(self):
        return (self.get_query_set().
                filter(published__lte=tz_now).
                order_by('-published'))

    def published_by_tag(self, tag):
        # Must this be a list?
        return self.published().filter(tags__slug=tag)


class Post(ContentArea):
    """
    Allow posts that aren't bound to a rigid template.
    """

    title = models.CharField(max_length=150)
    slug = models.SlugField(db_index=True, unique=True)
    published = models.DateTimeField(default=tz_now)
    author = models.ForeignKey(AUTH_USER_MODEL)

    objects = PostManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-published',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post', (), {'slug': self.slug})
