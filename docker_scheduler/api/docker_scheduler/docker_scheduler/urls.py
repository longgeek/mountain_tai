from django.conf.urls import patterns, include, url
from rest_framework import routers
from apphome import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)
router.register(r'hosts', views.HostViewSet)
router.register(r'containers', views.ContainerViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'docker_scheduler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
