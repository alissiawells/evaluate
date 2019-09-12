from django import forms

from .models import Evaluation
from .choises import RELEVANCE_CHOICES

class EvaluationForm(forms.Form):
    text_answer = forms.CharField(label='text answer', max_length=500)
    variants_answers = forms.ChoiceField(choices=RELEVANCE_CHOICES, widget=forms.RadioSelect,required=True)
    # class Meta:
    #     model = Evaluation
    #     fields = [
    #         "text_answer",
    #         "variants_answers"
    #     ]
