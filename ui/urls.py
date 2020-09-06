from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('project/<uuid:project_id>/',
         views.show_project, name='show_project'),
]
