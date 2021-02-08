from django.db import models
from django.db.models.deletion import PROTECT
from django.apps import apps as django_apps
from edc_base.model_mixins import BaseUuidModel


class MaternalDataset(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class AntenatalEnrollment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class MaternalDelivery(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class MaternalVisit(BaseUuidModel):

    appointment = models.ForeignKey(Appointment,
                         on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)


class CyhuuPreEnrollment(BaseUuidModel):

    maternal_visit = models.ForeignKey(MaternalVisit,
                         on_delete=PROTECT)

    biological_mother = models.CharField(max_length=3)


class HivRapidTestCounseling(BaseUuidModel):

    maternal_visit = models.ForeignKey(MaternalVisit,
                         on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    result = models.CharField(max_length=3)


