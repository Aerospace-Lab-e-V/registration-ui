from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from .models import Project, Candidate
from .forms import RegisterForm
from django.conf import settings
from .actions import successful_registration_action
from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()
# Create your views here.


def index(request):
    ''' Displays a List with all current and future registrations, which aren't full
    '''
    all_project = Project.objects.all().exclude(advertise=False)

    project_list = []
    for project in all_project:
        if check_if_registration_is_possible(project) and check_if_registration_is_in_future(project):
            project_list.append(project)

    active_project_list = []
    for project in project_list:
        if check_if_registration_is_active(project):
            active_project_list.append(project)

    project_list = [x for x in project_list if x not in active_project_list]

    context = {'active_projects': active_project_list,
               'future_projects': project_list}
    return render(request, 'ui/home.html', context)


def show_project(request, project_id):
    def get_form(project, *args):
        '''' select if form shows additional requirements '''
        return RegisterForm(*args,
                            requires_previous_year_membership=project.requires_previous_year_membership,
                            remove_application=(
                                not project.requires_application),
                            accept_covid=global_preferences['registration_covid'])

    project = Project.objects.get(project_id=project_id)

    if request.method == "POST":
        # RegisterForm(request.POST)
        form = get_form(project, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            # Check for double-entries
            if Candidate.objects.filter(forename=instance.forename, email=instance.email).count() == 0:
                instance.save()
            else:
                return render(request, 'ui/registration-failed.html')

            successful_registration_action(instance, project)
            return redirect('/project/{}/success'.format(project.project_id))
    else:
        form = get_form(project)

    context = {'project': project, 'form': form}

    if check_if_registration_is_active(project):
        if check_if_registration_is_possible(project):
            return render(request, 'ui/project-page.html', context)
        else:
            return render(request, 'ui/project-full.html', context)
    elif check_if_registration_is_in_future(project):
        return render(request, 'ui/registration-hasnt-started.html', context)


def registration_success(request, project_id):
    project = Project.objects.get(project_id=project_id)
    context = {'project': project}
    return render(request, 'ui/registration-success.html', context)


# -----------------------------------------------------------------------------
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
            if global_preferences['registration_opening_time'] > current_time:
                return False
        if project.registration_closing_date <= current_date:
            return False
    return True


def check_if_registration_is_in_future(project):
    ''' checks whether the registration-date is in the future(or now)
    '''
    current_date = timezone.localtime().date()

    if project.infinite_registration_period:
        return True
    # check if already closed
    if project.registration_closing_date <= current_date:
        return False
    else:
        return True


def check_if_registration_is_possible(project):
    ''' checks whether the maximum number of registrations has already been completed
    '''
    registered_users = project.candidate_set.all()
    max_registrations = project.max_registrations

    if len(registered_users) >= max_registrations:
        return False
    return True
