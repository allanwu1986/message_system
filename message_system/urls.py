from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from messages.views import user_login, user_page, user_logout, send_message

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'message_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', TemplateView.as_view(template_name='test.html')),
    url(r'^login/$', user_login),
    url(r'^user/([A-Za-z0-9]+)/$', user_page),
    url(r'^user/([A-Za-z0-9]+)/message/$', send_message),
    url(r'^logout/$', user_logout),
)
