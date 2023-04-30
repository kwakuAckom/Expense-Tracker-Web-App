import json
from django.utils.text import slugify
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ExpenseForm, CreateProjectForm, IncomeForm
from .models import Income, Project, Category, Expense
from django.views.generic import CreateView
from  django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Project, Expense
from django.views.decorators.csrf import csrf_exempt  # import the decorator
from django.core.exceptions import ValidationError

# This code imports the necessary modules and classes from Django to handle HTTP requests and render templates.

@login_required
def project_list(request):
    project_list = Project.objects.filter().order_by('-budget')
    paginator = Paginator(project_list,6)  # Create a Paginator object with 6 projects per page.
    page = request.GET.get('page')  # Retrieve the page number from the GET request parameters.
    try:
        project_list = paginator.page(page)  # Retrieve the corresponding page of projects.
    except PageNotAnInteger:
        project_list = paginator.page(1)  # If page is not an integer, deliver the first page.
    except EmptyPage:
        project_list = paginator.page(paginator.num_pages)  # If page is out of range (e.g. 9999), deliver the last page of results.
    return render(request, 'budget/project-list.html', {'project_list':project_list})

# This view displays a list of all projects, ordered by their budget in descending order.

@login_required
@csrf_exempt
def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)  # Retrieve the project object corresponding to the provided slug.
    if request.method == 'POST':
        form = ExpenseForm(request.POST)  # Create an expense form object with data from the POST request.
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        date = request.POST.get('date')
        category, _ = Category.objects.get_or_create(name=category_name, project=project)  # Retrieve or create the category object for the expense.
        _save = Expense.objects.create(
            project=project,
            title=title,
            amount=amount,
            category=category,
            description=description,
            priority=priority,
            date=date
        )  # Create a new expense object with the provided data.
        _save.save()  # Save the new expense object to the database.
        return redirect('detail', project_slug=project_slug)  # Redirect the user to the project detail page.
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']  # Retrieve the ID of the expense to delete from the request body.
        expense = get_object_or_404(Expense, id=id)  # Retrieve the expense object corresponding to the provided ID.
        expense.delete()  # Delete the expense object.
        return HttpResponse('')  # Return an empty HTTP response.
    else:
        expenses = Expense.objects.filter(project=project).order_by('-priority', '-date')  # Retrieve all expenses for the project, ordered by priority and date.
        context = {'project': project, 'expense_list': expenses, 'form': ExpenseForm()}  # Create a dictionary of context data to be passed to the template.
        return render(request, 'budget/project-detail.html', context)  # Render the project detail template with the context data.


@login_required
@csrf_exempt
def project_report(request):
    expenses = Expense.objects.filter().order_by('date')[:7]
    context = {'expense_list': expenses}
    return render(request, 'budget/reports.html', context)


 #view for the project creation page
class ProjectCreateView(CreateView):
    # set the model, template, and form fields for the view
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name','budget')

    # handle the form submission and creation of the project and categories
    def form_valid(self, form):
        # create a new project object with the submitted data but don't save it to the database yet
        self.object = form.save(commit=False)
        self.object.save()
        # get the category names from the submitted form data
        categories = self.request.POST['categoriesString'].split(',')
        # for each category name, create a new category object with the project and name and save it to the database
        for category in categories:
            Category.objects.create(
                project = Project.objects.get(id=self.object.id),
                name = category
            ).save()
        # redirect to the project list page
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('list')

# View for project deletion confirmation page
class DeleteConfirmationView(FormView):
    template_name = 'budget/confirm_delete.html'   # The template used to render the view
    form_class = None   # Form used is not specified
    
    # Get additional context data for rendering the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        return context
    
    # Get the URL to be redirected to after successful form submission
    def get_success_url(self):
        return reverse('delete', kwargs={'project_slug': self.kwargs['project_slug']})

# Delete a project
@login_required   # decorator to allow only authenticated users
@csrf_exempt   # decorator to allow cross-site request forgery protection to be bypassed
def delete_project(request, project_slug):
    # Get the project to be deleted
    project = get_object_or_404(Project, slug=project_slug)
    project.delete_project()   # Delete the project
    return redirect('list')   # Redirect to the project list page

# View for displaying a list of incomes
def income_list(request):
    incomes = Income.objects.all()   # Get all Income objects from the database
    return render(request, 'income-list.html', {'incomes': incomes})   # Render the income list template with the retrieved incomes

# View for displaying the details of an income
def income_detail(request, income_id):
    income = get_object_or_404(Income, pk=income_id)   # Get the Income object with the specified primary key
    return render(request, 'income-detail.html', {'income': income})   # Render the income detail template with the retrieved income

# View for creating a new income
def income_create(request):
    if request.method == 'POST':   # If the form is submitted
        form = IncomeForm(request.POST)   # Get the submitted form
        if form.is_valid():   # If the form is valid
            income = form.save()   # Save the new Income object to the database
            return redirect('income-detail', income_id=income.pk)   # Redirect to the detail page of the newly created income
    else:   # If the form is not submitted
        form = IncomeForm()   # Create a new, empty IncomeForm object
    return render(request, 'income-form.html', {'form': form})   # Render the income form template with the form object

# View for editing an existing income
def income_edit(request, income_id):
    income = get_object_or_404(Income, pk=income_id)   # Get the Income object to be edited
    if request.method == 'POST':   # If the form is submitted
        form = IncomeForm(request.POST, instance=income)   # Get the submitted form with the current income object as instance
        income = form.save()   # Save the updated Income object to the database
        return redirect('income-detail', income_id=income.pk)   # Redirect to the detail page of the edited income
    else:   # If the form is not submitted
        form = IncomeForm(instance=income)   # Create a new IncomeForm object pre-filled with the data from the income object
    return render(request, 'income-form.html', {'form': form})


def income_delete(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    income.delete()
    return redirect('income-list')

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income-list')
    else:
        form = IncomeForm()
    return render(request, 'income-form.html', {'form': form})
