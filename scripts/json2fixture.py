import os
import json
import codecs
import re
import csv
import sys
import datetime

def parseAnswers(answers):
    fix_answers = []
    for answer in answers:
        fix_answer = {
            'model' : 'evaluation.variantanswer',
            'pk' : answer['id'],
            'fields' : {
                'content' : answer['content'],
                'title' : answer['title'],
                'timestamp' : answer['timestamp'],
                'info_list' : json.dumps(answer['info_list'])
                }
        }
        fix_answers += [fix_answer]
    return fix_answers

def parseObjects(objects):
    fix_objects = []
    for obj in objects:
        fix_obj = {
            'model' : 'evaluation.evaluatedobject',
            'pk' : obj['id'],
            'fields' : {
                'content' : obj['content'],
                'title' : obj['title'],
                'timestamp' : obj['timestamp'],
                'info_list' : json.dumps(obj['info_list'])
                }
        }
        fix_objects += [fix_obj]
    return fix_objects

def parseTasks(tasks):
    fix_tasks = []
    for task in tasks:
        fix_task = {
            'model' : 'evaluation.task',
            'pk' : task['id'],
            'fields' : {
                'text_answer' : task['text_answer'],
                'task_type' : task['task_type_id'],
                'eval_object_id' : task['eval_object_id'],
                'variants_id' : json.dumps(task['variants_id'])
                }
        }
        fix_tasks += [fix_task]
    return fix_tasks

def parseTaskTypes(task_types):
    fix_instructions = []
    for task_type in task_types:
        fix_instruction = {
                'model' : 'evaluation.tasktype',
                'pk' : task_type['id'],
                'fields' : {
                    'name' : task_type['name'],
                    'instruction' : task_type['instruction'],
                    'timestamp' : task_type['timestamp'],
                    'choices' : json.dumps(task_type['choices']),
                    'default_choice' : task_type['default_choice'],
                    'number_of_assessments' : task_type['number_of_assessments'],
                    'random_order' : task_type['random_order'],
                    'show_text_answer_field': task_type['show_text_answer_field']
                }
        }
        fix_instructions += [fix_instruction]
    return fix_instructions

def parseEvaluations(evaluations):
    fix_evaluations = []
    for ev in evaluations:
        fix_ev = {
                'model' : 'evaluation.evaluation',
                'pk' : ev['id'],
                'fields' : {
                    'task_id' : ev['task_id'],
                    'assessor' : ev['assessor'],
                    'updated' : ev['updated'],
                    'created' : ev['created'],
                    'variants_answers' : json.dumps(ev['variants_answers']),
                    'text_answer' : ev['text_answer']
                }
        }
        fix_evaluations += [fix_ev]
    return fix_evaluations

if __name__ == "__main__":
    information = """
    Pass json file with data and name of output file as arguments to script:
    python json2fixture.py input_file output_file
    """
    if len(sys.argv) != 3:
        print(information)
        sys.exit()

    i_filename = sys.argv[1]
    o_filename = sys.argv[2]

    with codecs.open(i_filename,'r','utf-8') as f:
        data = json.load(f)

    fix_data = []
    fix_data.extend(parseObjects(data['evaluated_objects']))
    fix_data.extend(parseAnswers(data['answers']))
    fix_data.extend(parseTasks(data['tasks']))
    fix_data.extend(parseTaskTypes(data['task_types']))
    fix_data.extend(parseEvaluations(data['evaluations']))

    with codecs.open(o_filename, mode='w',encoding='utf-8') as f:
        f.write(json.dumps(fix_data))
