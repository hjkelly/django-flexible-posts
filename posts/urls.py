from django.conf.urls import patterns, include, url


urlpatterns = patterns('posts.views',
    # List all posts (only the published ones, of course).
    url(r'^posts/$', 'all_posts', name='all_posts'),

    # List published posts for a given tag, according to its slug.
    url(r'^tags/(?P<tag_slug>[\w\-]+)/$', 'posts_by_tag', name='posts_by_tag'),

    # Show the post itself.
    url(r'^posts/(?P<slug>[\w\-]+)/$', 'post', name='post'),
)
