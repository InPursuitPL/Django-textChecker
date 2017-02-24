from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.choice, name='choice'),
    url(r'^text_input/$', views.text_input, name='text_input'),
    url(r'^file_input/$', views.file_input, name='file_input'),
    #url(r'text_output/$', views.text_output, name='text_output')
]
