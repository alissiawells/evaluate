from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import EvaluatedObject
from .models import VariantAnswer
from .models import Task
from .models import Evaluation
from .models import TaskType
from .models import Assessor

class EvaluatedObjectModelAdmin(admin.ModelAdmin):
	list_display = ["title","timestamp"]
	search_fields = ["content", "title"]
	list_filter = ["timestamp"]
	class Meta:
		model = EvaluatedObject

class VariantAnswerModelAdmin(admin.ModelAdmin):
	list_display = ["title","timestamp"]
	search_fields = ["content", "title"]
	list_filter = ["timestamp"]
	class Meta:
		model = VariantAnswer

class TaskModelAdmin(admin.ModelAdmin):
	list_display = ["pk", "eval_object_id"]
	search_fields = ["eval_object_id"]
	class Meta:
		model = Task


class EvaluationModelAdmin(admin.ModelAdmin):
	list_display = ["pk","task_id","assessor","created","updated","is_rejected"]
	search_fields = ["pk", "assessor"]
	list_filter = ["created", "assessor", "task_id","updated"]
	class Meta:
		model = Evaluation

class TaskTypeModelAdmin(admin.ModelAdmin):
	list_display = ["name"]
	search_fields = ["name, instruction, timestamp"]
	list_filter = ["timestamp"]
	class Meta:
		model = TaskType

class AssessorInline(admin.StackedInline):
    model = Assessor
    can_delete = False
    verbose_name_plural = 'assessors'

class UserAdmin(BaseUserAdmin):
    inlines = (AssessorInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(EvaluatedObject,EvaluatedObjectModelAdmin)
admin.site.register(VariantAnswer,VariantAnswerModelAdmin)
admin.site.register(Task,TaskModelAdmin)
admin.site.register(Evaluation,EvaluationModelAdmin)
admin.site.register(TaskType,TaskTypeModelAdmin)
