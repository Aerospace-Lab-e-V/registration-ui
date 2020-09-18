from django.contrib import admin
from .models import Project, Candidate

# Register your models here.


class CandidateAdmin(admin.ModelAdmin):
    list_filter = ['project']
    list_display = ('forename', 'surname', 'project',
                    'email', 'school', 'school_class')


admin.site.register(Project)
admin.site.register(Candidate, CandidateAdmin)
