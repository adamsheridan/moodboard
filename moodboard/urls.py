from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'moodboard.views.index', name='index'),
    url(r'^add$', 'moodboard.views.createBoard', name='createBoard'),
    url(r'^(?P<slug>[\w\-]+)/$', 'moodboard.views.board', name='board'),
    url(r'^(?P<slug>[\w\-]+)/add$', 'moodboard.views.createImage', name='createImage'),
    url(r'^(?P<slug>[\w\-]+)/(?P<iid>\w{1,50})/comment$', 'moodboard.views.comments', name='comments'),
    url(r'^admin/', include(admin.site.urls)),
)
