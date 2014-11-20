from django.conf.urls import patterns, include, url
from rest_framework import routers
from apphome import views

from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
#router.register(r'images', views.ImageView)
#router.register(r'hosts', views.HostViewSet)
#router.register(r'containers', views.ContainerViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'docker_scheduler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include(router.urls)),

    url(r'^hosts/$',
        views.HostView.as_view()),

    url(r'^images/$',
        views.ImageView.as_view()),

    url(r'^containers/$',
        views.ContainerView.as_view()),

    url(r'^hosts/(?P<pk>[0-9]+)/$',
        views.HostDetailView.as_view()),

    url(r'^images/(?P<pk>[0-9]+)/$',
        views.ImageDetailView.as_view()),

    url(r'^containers/(?P<pk>[0-9]+)/$',
        views.ContainerDetailView.as_view()),

    url(r'^api-auth/',
        include('rest_framework.urls',
                namespace='rest_framework')),
)

urlpatterns = format_suffix_patterns(urlpatterns)
