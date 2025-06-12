from django import forms
from .models import QuizQuestion

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    (question.option_a, question.option_a),
                    (question.option_b, question.option_b),
                    (question.option_c, question.option_c),
                    (question.option_d, question.option_d),
                ],
                widget=forms.RadioSelect,
                required=True
            )
