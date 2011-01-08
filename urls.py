from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^survey/(?P<survey_id>\d+)/$', 'survey.surveybuilder.views.view'),
                       (r'^preview/(?P<survey_id>\d+)/$', 'survey.surveybuilder.views.preview'),
                   
                       (r'^email/(?P<survey_id>\d+)/$', 'survey.surveybuilder.views.email'),

                       (r'^new/$', 'survey.surveybuilder.views.create'),
                       (r'^add_question/(?P<survey_id>\d+)/$', 'survey.surveybuilder.views.add_question'),
                       
                       (r'^answer/(?P<survey_id>\d+)/$', 'survey.surveybuilder.views.answer'),

                       (r'^accounts/login/$',  login),
                       (r'^accounts/logout/$', logout),
                       
                       (r'^accounts/profile/$', 'survey.surveybuilder.views.list'),
                       (r'^$', 'survey.surveybuilder.views.list'),
                       (r'^list/$', 'survey.surveybuilder.views.list'),
                       (r'^accounts/$', 'survey.surveybuilder.views.list'),
                       

    # Example:
    # (r'^survey/', include('survey.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
