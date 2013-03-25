from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'resttuto.views.home', name='home'),
    # url(r'^resttuto/', include('resttuto.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # REST framework (http://django-rest-framework.org)
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # REST framework tutorial
    url(r'^', include('snippets.urls')),
)
