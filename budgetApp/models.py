from datetime import date, timedelta
from itertools import count
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


class Income(models.Model):
    FREQUENCY_CHOICES = (
        (1, 'Weekly'),
        (2, 'Monthly'),
        (3, 'Annually')
    )

    title = models.CharField(max_length=30)
    description = models.TextField(max_length=60 )
    amount = models.PositiveSmallIntegerField(default=0.00)
    frequency = models.PositiveSmallIntegerField(choices=FREQUENCY_CHOICES, default=1)
    last_updated = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the next update date based on the frequency and last_updated date
        next_update_date = self.last_updated
        if self.frequency == 1:
            next_update_date += timedelta(days=7)
        elif self.frequency == 2:
            next_update_date += timedelta(days=30)
        elif self.frequency == 3:
            next_update_date += timedelta(days=365)

        # Check if the current date is greater than or equal to the next update date
        if date.today() >= next_update_date:
            # Update the income amount and last_updated date
            self.amount += self.amount * self.frequency / 100
            self.last_updated = date.today()

        super().save(*args, **kwargs)
        
class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    income_source = models.ForeignKey(Income, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.income_source and self.income_source.amount > self.budget:
            raise ValidationError("Income source amount cannot be greater than the budget.")
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def delete_project(self):
        self.delete()

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())
    def get_total(self):
        return count(expense.amount for expense in self.expenses.all())

    def get_left(self):
        total_expenses = self.expenses.aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.budget - total_expenses


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise Exception("Cannot delete default category.")
        super(Category, self).delete(*args, **kwargs)


class Expense(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=30 )
    amount = models.PositiveSmallIntegerField(default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)



    
