from django import forms
from .models import Category, Expense, Project



# class ExpenseForm(forms.Form):
#     title = forms.CharField()
#     amount = forms.NumberInput()
#     category = forms.CharField()

class ExpenseForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.none())

    class Meta:
        model = Expense
        fields = ['title', 'description', 'amount', 'category', 'priority']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['category'].queryset = Category.objects.filter(project=project)

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'budget','income_source']
