from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # The homepage should just show all posts, so redirect them there.
    url(r'^$', RedirectView.as_view(url='/posts/'), name='home'),

    # Include the standard URLs at the top level.
    url(r'', include('posts.urls')),
)
