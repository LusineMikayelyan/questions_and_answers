from django import forms


class QuestionForm(forms.Form):
    question_field = forms.CharField(label='Question',
                                     widget=forms.Textarea(attrs={"rows": 1, "cols": 12}))
