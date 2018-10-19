from django.conf.urls import url
from . import views  

urlpatterns = [
    url(r'^$', views.default),
    url(r'^regcheck', views.add_user),
    url(r'^success', views.logged),
    url(r'^check', views.check),
    url(r'^createjob', views.jobcreate),
    url(r'^logjob', views.logjob),
    url(r'^logout',views.logout),
    url(r'^(?P<number>\d+)/view$', views.viewjob),
    url(r'^(?P<number>\d+)/add', views.addjob),
    url(r'^(?P<number>\d+)/edit', views.editjob),
    url(r'^(?P<number>\d+)/cancel', views.canceljob),
    url(r'^(?P<number>\d+)/viewmyjob', views.viewmyjob),
    url(r'^(?P<number>\d+)/jobfinish', views.finishjob),
    url(r'^makeedit', views.makeedit),
]