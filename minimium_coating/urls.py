from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minimium_coating.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Home app
    url(r'^$', 'minimium_coating.views.home', name='home'),

    # calculate minimium coating
    url(
        r'^calcular-recubrimiento-minimo/$',
        'minimium_coating.views.calculate_minimium_coating',
        name='calculate_minimium_coating'
    ),

    url(r'^admin/', include(admin.site.urls)),
)
