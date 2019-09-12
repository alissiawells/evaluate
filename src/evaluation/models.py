from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from choises import RELEVANCE_CHOICES
from django.http import HttpResponse, HttpResponseRedirect

import json

class EvaluatedObject(models.Model):
    title = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    content = models.TextField(default="")
    # json field
    info_list = models.TextField(default="\"[]\"")

    def get_pk(self):
        return self.pk

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    # @property
    def get_info_list(self):
        return json.loads(self.info_list)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("evaluation:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp"]

class VariantAnswer(models.Model):
    title = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    content = models.TextField(default="")
    # json field
    info_list = models.TextField(default="\"[]\"")

    def get_pk(self):
        return self.pk

    def get_info_list(self):
        return json.loads(self.info_list)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("evaluation:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp"]


class Task(models.Model):
    eval_object_id = models.IntegerField()
    task_type = models.IntegerField()
    variants_id = models.TextField(default="")
    text_answer = models.BooleanField(default=False)

    def get_pk(self):
        return self.pk

    # @property
    def get_eval_object_id(self):
        return self.eval_object_id

    def get_task_type(self):
        return self.task_type

    def set_task_type(self, tt):
        self.get_task_type = tt

    # @property
    def get_text_answer(self):
        return self.text_answer

    # @property
    def get_variants_id(self):
        return json.loads(self.variants_id)

    def __str__(self):
        return str(self.eval_object_id)

    def __unicode__(self):
        return unicode(self.eval_object_id)

class Evaluation(models.Model):
    task_id = models.IntegerField()
    assessor = models.CharField(max_length=80, default="")
    is_rejected = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    # json strings
    variants_answers = models.TextField(default="")
    # usual strngs
    text_answer = models.TextField(default="")

    # @authors.setter
    def set_variants_answers(self, answers_list):
        self.variants_answers = json.dumps(answers_list)

    def set_assessor(self, assessor):
        self.assessor = assessor

    def set_is_rejected(self, flag):
        self.is_rejected = flag

    def set_text_answer(self, text_answer):
        self.text_answer = text_answer

    def set_task_id(self, task_id):
        self.task_id = task_id

    def get_updated(self):
        return self.updated

    def get_task_id(self):
        return self.task_id

    def get_variants_answers(self):
        return json.loads(self.variants_answers)

    def get_text_answer(self):
        return self.text_answer

    def get_is_rejected(self):
        return self.is_rejected

class TaskType(models.Model):
    name = models.CharField(max_length=200,default="")
    instruction = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    choices = models.TextField(default=json.dumps(RELEVANCE_CHOICES))
    default_choice = models.CharField(max_length=200, default=RELEVANCE_CHOICES[0][0])
    number_of_assessments = models.IntegerField(default=1)
    random_order = models.BooleanField(default=True)
    show_text_answer_field = models.BooleanField(default=True)

    def get_instruction(self):
        return self.instruction

    def get_pk(self):
        return self.pk

    def get_pk_str(self):
        return str(self.pk)

    def get_choices(self):
        return json.loads(self.choices)

    def get_show_text_answer_field(self):
        return self.show_text_answer_field

    def is_random_order(self):
        return self.random_order

    def get_number_of_assessments(self):
        return self.number_of_assessments

    def get_default_choice(self):
        return self.default_choice

    def get_name(self):
        return self.name

    class Meta:
        ordering = ["-timestamp"]
        # get_latest_by = 'timestamp'

class Assessor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chosen_task_type = models.IntegerField(default=1)

    def set_chosen_task_type(self, tt):
        self.chosen_task_type = tt

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Assessor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.assessor.save()
