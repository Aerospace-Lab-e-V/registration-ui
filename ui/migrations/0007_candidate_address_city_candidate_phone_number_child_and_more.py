# Generated by Django 4.2.5 on 2023-09-11 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_rename_address_candidate_address_street_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='address_city',
            field=models.CharField(default='-', max_length=70, verbose_name='Ort, PLZ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='phone_number_child',
            field=models.CharField(blank=True, max_length=17, null=True, verbose_name='Telefonnummer Teilnehmer*in'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='address_street',
            field=models.CharField(max_length=70, verbose_name='Straße, Hausnummer'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone_number',
            field=models.CharField(max_length=17, verbose_name='Telefonnummer Elternteil'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='school',
            field=models.CharField(max_length=40, verbose_name='Schule / Uni / ...'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='school_class',
            field=models.CharField(max_length=10, verbose_name='Klasse / Semester'),
        ),
    ]