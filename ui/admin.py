from django.contrib import admin
from .models import Project, Candidate

# Register your models here.


class CandidateAdmin(admin.ModelAdmin):
    list_filter = ['project']
    list_display = ('forename', 'surname', 'project',
                    'email', 'school', 'school_class')
    search_fields = ['surname', 'forename']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'registration_starting_date')
    list_filter = ['day', 'registration_starting_date']
    search_fields = ['name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Candidate, CandidateAdmin)
