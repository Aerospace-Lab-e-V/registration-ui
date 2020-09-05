import uuid
from django.db import models

# Create your models here.


class Candidate(models.Model):
    ''' Model for every candidate
    '''
    candidate_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    forename = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.surname, self.forename)


class Project(models.Model):
    ''' Model for every project
    '''
    project_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=60)
    note = models.TextField('Beschreibung', max_length=300, blank=True)

    max_registrations = models.DecimalField(
        'Max. Teilnehmeranzahl', max_digits=2, decimal_places=0)
    registration_closing_date = models.DateField(blank=True, null=True)
    candidates = models.ManyToManyField(Candidate, related_name="candidates")
    confirmed_candidates = models.ManyToManyField(
        Candidate, related_name="confirmed_candidates")
    DAYS_OF_WEEK = [
        ('Mo', 'Montag'),
        ('Di', 'Dienstag'),
        ('Mi', 'Mittwoch'),
        ('Do', 'Donnerstag'),
        ('Fr', 'Freitag'),
        ('Sa', 'Sammstag'),
        ('So', 'Sonntag')
    ]
    day = models.CharField(
        max_length=2,
        choices=DAYS_OF_WEEK,
        default='MO',
    )

    def __str__(self):
        return '{}'.format(self.name)
