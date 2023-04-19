from django import forms
from .models import Expense, Project



# class ExpenseForm(forms.Form):
#     title = forms.CharField()
#     amount = forms.NumberInput()
#     category = forms.CharField()

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        # fields = ('title', 'amount', 'category')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount:
            raise forms.ValidationError("Amount field is required.")
        try:
            amount = float(amount)
        except ValueError:
            raise forms.ValidationError("Amount must be a valid number.")
        return amount

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'budget','income_source']
