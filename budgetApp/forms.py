from django import forms
from django.shortcuts import redirect, render
from .models import Category, Expense, Project, Income




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
        print(args, kwargs)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['category'].queryset = Category.objects.filter(project=project)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        category = cleaned_data.get('category')
        project = category.project if category else None
        if project and amount:
            remaining_budget = project.budget - Expense.objects.filter(category__project=project).exclude(pk=self.instance.pk).aggregate(models.Sum('amount'))['amount__sum'] or 0
            if amount > remaining_budget:
                raise forms.ValidationError(f"Expense amount ({amount}) exceeds remaining budget ({remaining_budget}).")


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'budget','income_source']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['title', 'description', 'amount', 'frequency']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }