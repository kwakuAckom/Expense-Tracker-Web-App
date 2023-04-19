from django.contrib import admin
from .models import Project, Expense, Category, Income
# Register your models here.

admin.site.register(Project)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Category)