from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.models import User

import json
import random
from evaluateme.settings import STATIC_ROOT

# Create your views here.
from .models import Evaluation, Task, VariantAnswer, EvaluatedObject, TaskType, Assessor
from .forms import EvaluationForm
from .choises import RELEVANCE_CHOICES

@login_required(login_url='/accounts/login/')
def eval_form(request,task_id=None):
    task_type_id = request.user.assessor.chosen_task_type
    tasktype = get_object_or_404(TaskType, pk=task_type_id)
    relevance_choices = tasktype.get_choices()
    default_answer = tasktype.get_default_choice()
    APPROPRIATE_NUMBER_OF_ASSESSMENTS = tasktype.get_number_of_assessments()
    random_order = tasktype.is_random_order()
    show_text_answer_field = tasktype.get_show_text_answer_field()

    already_evaluated_by_me = [obj.get_task_id() for obj in Evaluation.objects.filter(assessor=request.user)]
    already_evaluated_by_me = [task.get_pk() for task in Task.objects.filter(pk__in=already_evaluated_by_me) if task_type_id == task.get_task_type()]
    if task_id is None:
        task = None
        already_evaluated = [obj.get_task_id() for obj in Evaluation.objects.all()]
        already_evaluated = [task.get_pk() for task in Task.objects.filter(pk__in=already_evaluated) if task_type_id == task.get_task_type()]
        tmp_dict = {}
        tmp_list = []
        for tid in already_evaluated:
            tmp_dict.setdefault(tid,0)
            tmp_dict[tid] += 1
        for tid,v in tmp_dict.items():
            if v < APPROPRIATE_NUMBER_OF_ASSESSMENTS and tid not in already_evaluated_by_me:
                tmp_list += [tid]
        if tasktype.is_random_order():
            if tmp_list and random.random() < 0.75:
                task_id = tmp_list[random.randint(0,len(tmp_list))-1]
                task = get_object_or_404(Task,pk=task_id)
            else:
                tasks = [t for t in Task.objects.all() if t.get_pk() not in already_evaluated_by_me and t.get_task_type() == task_type_id]
                if not tasks:
                    return HttpResponseRedirect("/evaluation/thanks/")
                task = tasks[random.randint(0,len(tasks))-1]
        else:
            tasks = sorted([t for t in Task.objects.all() if t.get_pk() not in already_evaluated_by_me and t.get_task_type() == task_type_id],
                           key=lambda x: x.get_pk())
            if not tasks:
                return HttpResponseRedirect("/evaluation/thanks/")
            task = tasks[0]
        return HttpResponseRedirect("/evaluation/eval_form/{0}/".format(task.get_pk()))
        # variants_id = task.get_variants_id()
    else:
        if task_id in already_evaluated_by_me:
            return HttpResponseRedirect("/evaluation/info_already_evaluated/{0}/".format(task_id))
        task = get_object_or_404(Task,pk=task_id)

    variants_id = task.get_variants_id()
    eval_object = get_object_or_404(EvaluatedObject,pk=task.get_eval_object_id())
    variants = []
    if len(VariantAnswer.objects.all()):
        variants = [get_object_or_404(VariantAnswer,pk=var_id) for var_id in variants_id]
    else:
        variants = [get_object_or_404(EvaluatedObject,pk=var_id) for var_id in variants_id]

    given_answers = [eval.get_text_answer() for eval in Evaluation.objects.filter(task_id=task_id)]
    tmp_dict = {}
    for answ in given_answers:
        if not len(answ):
            continue
        tmp_dict.setdefault(answ,0)
        tmp_dict[answ] += 1
    given_answers = [k for k,v in sorted(tmp_dict.items(),key=lambda x: x[1])[::-1]]

    valid_form = True
    if request.method == 'POST':
        is_rejected = bool(request.POST.get(u'reject',u""))
        if Evaluation.objects.filter(assessor=request.user,task_id=task_id):
            return HttpResponseRedirect("/evaluation/info_already_evaluated/{0}/".format(task_id))
        if not is_rejected:
            for var in variants:
                if unicode(var.get_pk()) not in request.POST:
                    valid_form = False
                    break
                if show_text_answer_field and task.get_text_answer() and len(request.POST['text_answer']) == 0:
                    valid_form = False
        if valid_form:
            instance = Evaluation()
            instance.set_is_rejected(is_rejected)
            instance.set_assessor(request.user)
            instance.set_task_id(task_id)
            if show_text_answer_field:
                instance.set_text_answer(request.POST['text_answer'])
            answers = [request.POST[unicode(var.get_pk())] for var in variants]
            instance.set_variants_answers(answers)
            instance.set_assessor(request.user)
            instance.save()
            messages.success(request,"Evaluation is added!")
            return HttpResponseRedirect("/evaluation/eval_form/")
        else:
            messages.success(request,"Error. Some fields is not fiiled out")
            return HttpResponseRedirect("/evaluation/eval_form/{0}/".format(task.get_pk()))


    context = {
        # "form": form,
        'eval_object' : eval_object,
        'variants' : variants,
        'choises' : relevance_choices,
        'given_answers' : given_answers,
        'show_text_answer_field' : show_text_answer_field,
        'textAnswer' : task.get_text_answer(),
        'default_answer' : default_answer,
        'is_rejected' : False,
        'task_type' : str(task.get_task_type()),
        'task_types' : TaskType.objects.all()
    }
    return render(request,"eval_form.html",context)

@login_required(login_url='/accounts/login/')
def edit_eval(request,task_id=None):
    evaluation = get_object_or_404(Evaluation,assessor=request.user,task_id=task_id)
    task_id = evaluation.get_task_id()
    task = get_object_or_404(Task,pk=task_id)

    tasktype = get_object_or_404(TaskType, pk=task.get_task_type())
    show_text_answer_field = tasktype.get_show_text_answer_field()

    variants_id = task.get_variants_id()
    eval_object = get_object_or_404(EvaluatedObject,pk=task.get_eval_object_id())
    variants = []
    if len(VariantAnswer.objects.all()):
        variants = [get_object_or_404(VariantAnswer,pk=var_id) for var_id in variants_id]
    else:
        variants = [get_object_or_404(EvaluatedObject,pk=var_id) for var_id in variants_id]

    given_answers = [eval.get_text_answer() for eval in Evaluation.objects.filter(task_id=task_id)]
    tmp_dict = {}
    for answ in given_answers:
        if not len(answ):
            continue
        tmp_dict.setdefault(answ,0)
        tmp_dict[answ] += 1
    given_answers = [k for k,v in sorted(tmp_dict.items(),key=lambda x: x[1])[::-1]]

    valid_form = True
    if request.method == 'POST':
        is_rejected = bool(request.POST.get(u'reject',u""))
        if not is_rejected:
            for var in variants:
                if unicode(var.get_pk()) not in request.POST:
                    valid_form = False
                    break
                if show_text_answer_field and task.get_text_answer() and len(request.POST['text_answer']) == 0:
                    valid_form = False
                    break
        if valid_form:
            evaluation.set_is_rejected(is_rejected)
            if show_text_answer_field:
                evaluation.set_text_answer(request.POST['text_answer'])
            answers = [request.POST[unicode(var.get_pk())] for var in variants]
            evaluation.set_variants_answers(answers)
            evaluation.save()
            messages.success(request,"Saved!")
            return HttpResponseRedirect("/evaluation/edit_eval/{0}/".format(task_id))
        else:
            messages.success(request,"Error. Some fields is not fiiled out")
            return HttpResponseRedirect("/evaluation/edit_eval/{0}/".format(task.get_pk()))

    relevance_choices = tasktype.get_choices()
    context = {
        # "form": form,
        'eval_object' : eval_object,
        'variants' : zip(variants,evaluation.get_variants_answers()),
        'choises' : relevance_choices,
        'given_answers' : given_answers,
        'show_text_answer_field' : show_text_answer_field,
        'textAnswer' : task.get_text_answer(),
        'default_text_answer' : evaluation.get_text_answer(),
        'is_rejected' : evaluation.get_is_rejected(),
        'task_type' : str(task.get_task_type()),
        'task_types' : TaskType.objects.all()
    }
    return render(request,"edit_eval.html",context)


@login_required(login_url='/accounts/login/')
def info_already_evaluated(request,task_id=None):
    context = {
        'task_id' : task_id,
        'task_type' : str(request.user.assessor.chosen_task_type),
        'task_types' : TaskType.objects.all()
    }
    return render(request,"info_already_evaluated.html",context)

@login_required(login_url='/accounts/login/')
def evaluated_list(request):
    evals = Evaluation.objects.filter(assessor=request.user.username).order_by('-updated')
    ev_obj = []
    for ev in evals:
        try:
            task = Task.objects.get(pk=ev.get_task_id())
            if task.get_task_type() == request.user.assessor.chosen_task_type:
                ev_obj += [(
                    ev,
                    EvaluatedObject.objects.get(pk=task.get_eval_object_id())
                    )]
        except:
            continue

    show_text_answer_field = get_object_or_404(TaskType, pk=request.user.assessor.chosen_task_type).get_show_text_answer_field()

    context = {
        "evaluated_list": ev_obj,
        "user" : request.user,
        'task_type' : str(request.user.assessor.chosen_task_type),
        'task_types' : TaskType.objects.all(),
        'show_text_answer_field' : show_text_answer_field
    }
    return render(request,"evaluated_list.html",context)

@login_required(login_url='/accounts/login/')
def instructions(request):
    if request.method == 'POST':
        tt = request.POST["task_type_select"]
        try:
            task_type = TaskType.objects.get(pk=tt)
            request.user.assessor.chosen_task_type = tt
            request.user.save()
            msg = u"Selected task type: "+task_type.get_name()
            messages.success(request,msg)
        except:
            msg = u"There is no such task type: "+unicode(tt)
            messages.error(request,msg)

    tt = request.user.assessor.chosen_task_type
    task_type = TaskType.objects.get(pk=tt)
    context = {
        'task_type' : str(request.user.assessor.chosen_task_type),
        'task_types' : TaskType.objects.all(),
        'instruction' : task_type.get_instruction()
    }
    return render(request,"instructions.html",context)

@login_required(login_url='/accounts/login/')
def thanks(request):
    context = {
        "user": request.user,
        'task_type' : str(request.user.assessor.chosen_task_type),
        'task_types' : TaskType.objects.all()
    }
    return render(request,"thanks.html",context)
