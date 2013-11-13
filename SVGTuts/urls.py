from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SVGTuts.views.home', name='home'),
    # url(r'^SVGTuts/', include('SVGTuts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Tutorien
    url(r'^$','tutorien.views.index'),
    url(r'^login/$', 'tutorien.views.LoginRequest'),
    url(r'^logout/$', 'tutorien.views.LogoutRequest'),
    url(r'^Tutorien/$', 'tutorien.views.GetTuts'),
    url(r'^Erstellen/$', 'tutorien.views.CreateTut'),
    url(r'^Erstellen2/$', 'tutorien.views.CreateTut2'),
    url(r'^Benutzer/$', 'tutorien.views.manageUsers'),
    url(r'^Bewerben/$','tutorien.views.CreateTutorSuggestion'),
    url(r'^meineDaten/$','tutorien.views.MyData'),
    url(r'^Bewerbungen/$', 'tutorien.views.getSuggestions')
)
