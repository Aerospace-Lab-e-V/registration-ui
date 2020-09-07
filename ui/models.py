import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone

# Create your models here.


class Project(models.Model):
    ''' Model for every project
    '''
    project_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Name', max_length=60)
    note = models.TextField('Beschreibung', max_length=300, blank=True)

    max_registrations = models.DecimalField(
        'Max. Teilnehmeranzahl', max_digits=2, decimal_places=0, default=10)
    registration_starting_date = models.DateField(
        'Datum: Öffnung der Registrierung', default=timezone.now)
    registration_closing_date = models.DateField(
        'Datum: Schließung der Registrierung', default=timezone.now() + timedelta(days=365))
    infinite_registration_period = models.BooleanField(
        'Unbegrenz lange Registrieungsphase', default=False)

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
        'Tag',
        max_length=2,
        choices=DAYS_OF_WEEK,
        blank=True,
        null=True
    )
    advertise = models.BooleanField('Bewerbung des Projekts', default=True,
                                    help_text="Zeigt das Projekt in der List auf der Startseite an")

    def __str__(self):
        return '{}'.format(self.name)


class Candidate(models.Model):
    ''' Model for every candidate
    '''
    candidate_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    forename = models.CharField('Vorname', max_length=25)
    surname = models.CharField('Nachname', max_length=25)
    email = models.EmailField('E-Mail', max_length=50)

    school = models.CharField('Schule', max_length=40)
    school_class = models.CharField('Klasse', max_length=5)

    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                # necessary, so the custom form-function can insert it after the sumbit
                                blank=True, null=True)
    approved = models.BooleanField("Angenommen", default=False)

    def __str__(self):
        return '{}, {}'.format(self.surname, self.forename)
