from django.conf.urls import url, include
from django.contrib import admin

from evaluation.views import (
	instructions,
	eval_form,
    thanks,
    info_already_evaluated,
    edit_eval,
	evaluated_list,
)

urlpatterns = [
    url(r'^info_already_evaluated/(?P<task_id>\d+)/$', info_already_evaluated, name='info_already_evaluated'),
    url(r'^thanks/$', thanks, name='thanks'),
    url(r'^instructions/$', instructions, name='instructions'),
    url(r'^evaluated_list/$', evaluated_list, name='evaluated_list'),
    url(r'^edit_eval/(?P<task_id>\d+)/$', edit_eval, name='edit_eval'),
    url(r'^edit_eval/$', edit_eval, name='edit_eval'),
    url(r'^eval_form/(?P<task_id>\d+)/$', eval_form, name='eval_form_by_id'),
    url(r'^eval_form/$', eval_form, name='eval_form'),
    url(r'^.*$', instructions, name='instructions'),
]
