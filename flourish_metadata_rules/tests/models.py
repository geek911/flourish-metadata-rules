from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel


class MaternalDataset(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    delivdt = models.DateField(null=True, blank=True)


class ChildDataset(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class ChildAssent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    dob = models.DateField(null=True, blank=True)

    gender = models.CharField(max_length=1)


class ChildDummyConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    dob = models.DateField(null=True, blank=True)


class AntenatalEnrollment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class MaternalDelivery(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    delivery_datetime = models.DateTimeField(null=True, blank=True)

    live_infants_to_register = models.IntegerField()


class MaternalVisit(BaseUuidModel):

    appointment = models.ForeignKey(Appointment,
                                    on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)


class ChildVisit(BaseUuidModel):

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
