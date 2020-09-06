from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Project
from .forms import RegisterForm

# Create your views here.


def index(request):
    all_project = Project.objects.all()

    advertised_projects = []
    for project in all_project:
        if project.advertise:
            if project.infinite_registration_period:
                advertised_projects.append(project)
            else:
                # necessary if one didn't enter any date without infinite_registration
                try:
                    if project.registration_closing_date >= timezone.now:
                        advertised_projects.append(project)
                except:
                    # fails to a display
                    advertised_projects.append(project)

    context = {'projects': advertised_projects}
    return render(request, 'ui/home.html', context)


def show_project(request, project_id):
    project = Project.objects.get(project_id=project_id)
    registered_users = project.candidate_set.all()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()

            return redirect('/sucess/')
    else:
        form = RegisterForm()

    context = {'project': project, 'form': form}

    if len(registered_users) >= project.max_registrations:
        return render(request, 'ui/project-full.html', context)

    return render(request, 'ui/project-page.html', context)
