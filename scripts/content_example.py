# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31

@author: angriff07@gmail.com
"""

import json
import codecs
import datetime
import numpy as np

evaluated_objects = []
for idx in xrange(100):
    i = idx+1
    obj = {}
    obj['id'] = i
    obj['title'] = 'title_'+str(i)
    obj['content'] = 'content'+str(i)
    obj['timestamp'] = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%S+00:00")
    obj['info_list'] = []
    for j in xrange(3):
        obj['info_list'] += ['info field '+str(j+1)+' of obj '+str(i)]
    evaluated_objects += [obj]

answers = []
for idx in xrange(100):
    i = idx + 1
    obj = {}
    obj['id'] = i
    obj['title'] = 'title_'+str(i)
    obj['content'] = 'content answ '+str(i)
    obj['timestamp'] = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%S+00:00")
    obj['info_list'] = []
    for j in xrange(2):
        obj['info_list'] += ['info field '+str(j+1)+' of answ '+str(i)]
    answers += [obj]

tasks = []
for j,eval_obj in enumerate(evaluated_objects):
    i = j + 1
    t = {}
    t['id'] = i
    t['text_answer'] = False
    if np.random.rand() < 0.5:
        t['text_answer'] = True
    t['variants_id'] = []
    t['eval_object_id'] = eval_obj['id']
    for idx in np.random.permutation(range(len(answers)))[:3]:
        # print answers[idx]['id']
        t['variants_id'] += [answers[idx]['id']]
    tasks += [t]

# leave empty if u don't have alredy evaluated tasks
evaluations = []

instructions = []
instr = {
    'id' : 1,
    'content' : u"Here is instruction for assessors!",
    'timestamp' :  datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%S+00:00")
}
instructions += [instr]

data = {
    'instructions' : instructions,
    'evaluated_objects' : evaluated_objects,
    'answers' : answers,
    'tasks' : tasks,
    'evaluations' : evaluations
}

with codecs.open("test.json",'w','utf-8') as f:
    json.dump(data,f)
