from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'robots_wars.views.home', name='home'),
    # url(r'^robots_wars/', include('robots_wars.foo.urls')),


    url(r'^login/$',  'django.contrib.auth.views.login', {'template_name': 'authent/login.html'} , name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login' , name="logout"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('maingame.urls')),
)
