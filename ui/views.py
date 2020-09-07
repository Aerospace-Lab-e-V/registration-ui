from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from .models import Project
from .forms import RegisterForm
from django.conf import settings

# Create your views here.


def index(request):
    ''' Displays a List with all current and future registrations, which aren't full
    '''
    current_date = timezone.localtime().date()

    all_project = Project.objects.filter(
        registration_closing_date__gt=current_date
    ).exclude(advertise=False)

    project_list = []
    for project in all_project:
        if check_if_registration_is_possible(project):
            project_list.append(project)

    active_project_list = []
    for project in project_list:
        if check_if_registration_is_active(project):
            active_project_list.append(project)
            project_list.remove(project)

    context = {'active_projects': active_project_list,
               'future_projects': project_list}
    return render(request, 'ui/home.html', context)


def show_project(request, project_id):
    project = Project.objects.get(project_id=project_id)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()

            return redirect('/sucess/')
    else:
        form = RegisterForm()

    context = {'project': project, 'form': form}

    if check_if_registration_is_active(project):
        if check_if_registration_is_possible:
            return render(request, 'ui/project-page.html', context)
        else:
            return render(request, 'ui/project-full.html', context)

    return render(request, 'ui/registration-closed.html', context)


# helper-functions
def check_if_registration_is_active(project):
    ''' checks whether the registration is open or closed
    '''
    current_date = timezone.localtime().date()
    current_time = timezone.localtime().time()

    # skips timing-based checks for infinite_registration_period
    if not project.infinite_registration_period:
        if project.registration_starting_date > current_date:
            return False
        elif project.registration_starting_date == current_date:
            if settings.REGISTRATION_OPENING_TIME > current_time:
                return False
        if project.registration_closing_date <= current_date:
            return False
    return True


def check_if_registration_is_possible(project):
    ''' checks whether the maximum number of registrations has already been completed
    '''
    registered_users = project.candidate_set.all()
    max_registrations = project.max_registrations

    if len(registered_users) >= max_registrations:
        return False
    return True
