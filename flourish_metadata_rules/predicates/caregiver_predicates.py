from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.utils import age, get_utcnow
from edc_constants.constants import POS, YES
from edc_metadata_rules import PredicateCollection
from flourish_caregiver.helper_classes import MaternalStatusHelper
from dateutil.relativedelta import relativedelta


class CaregiverPredicates(PredicateCollection):

    app_label = 'flourish_caregiver'
    pre_app_label = 'pre_flourish'
    visit_model = f'{app_label}.maternalvisit'

    def pregnant(self, visit=None, **kwargs):
        """Returns true if expecting
        """
        enrollment_model = django_apps.get_model(f'{self.app_label}.antenatalenrollment')
        try:
            enrollment_model.objects.get(subject_identifier=visit.subject_identifier)
        except enrollment_model.DoesNotExist:
            return False
        else:
            maternal_delivery_cls = django_apps.get_model(f'{self.app_label}.maternaldelivery')
            try:
                maternal_delivery_cls.objects.get(subject_identifier=visit.subject_identifier)
            except maternal_delivery_cls.DoesNotExist:
                return True
        return False

    def prior_participation(self, visit=None, **kwargs):
        maternal_dataset_model = django_apps.get_model(f'{self.app_label}.maternaldataset')

        try:
            maternal_dataset_model.objects.get(subject_identifier=visit.subject_identifier)
        except maternal_dataset_model.DoesNotExist:
            return False
        else:
            return True

    def func_preg_no_prior_participation(self, visit=None, **kwargs):
        """Returns true if participant is expecting and never
        participated in a BHP study for enrollment_visit.
        """
        return self.pregnant(visit=visit) and not self.prior_participation(visit=visit)

    def func_caregiver_no_prior_participation(self, visit=None, **kwargs):
        """Returns true if participant is a caregiver and never participated in a BHP study.
        """
        return not self.pregnant(visit=visit) and not self.prior_participation(visit=visit)

    def func_bio_mother(self, visit=None, **kwargs):
        consent_cls = django_apps.get_model(f'{self.app_label}.subjectconsent')

        consent_obj = consent_cls.objects.filter(
                subject_identifier=visit.subject_identifier,).latest('created')

        return consent_obj.biological_caregiver == YES

    def func_bio_mothers_hiv(self, visit=None,
                             maternal_status_helper=None, **kwargs):
        """Returns true if participant is biological mother living with HIV.
        """
        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        if self.pregnant(visit=visit):
            return maternal_status_helper.hiv_status == POS
        else:
            return (self.func_bio_mother(visit=visit)
                    and maternal_status_helper.hiv_status == POS)

    def func_pregnant_hiv(self, visit=None,
                          maternal_status_helper=None, **kwargs):
        """Returns true if a newly enrolled participant is pregnant and living with HIV.
        """
        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        return (self.pregnant(visit=visit)
                and maternal_status_helper.hiv_status == POS)

    def func_non_pregnant_caregivers(self, visit=None, **kwargs):
        """Returns true if non pregnant.
        """
        return not self.pregnant(visit=visit)

    def func_newly_recruited(self, visit=None, **kwargs):
        cyhuu_model_cls = django_apps.get_model(
                f'{self.pre_app_label}.cyhuupreenrollment')
        try:
            cyhuu_model_cls.objects.get(
                maternal_visit__appointment__subject_identifier=visit.subject_identifier)
        except cyhuu_model_cls.DoesNotExist:
            return False
        else:
            return True

    def func_LWHIV_aged_10_15(self, visit=None, **kwargs):
        consent_onbehalf_cls = django_apps.get_model(
                f'{self.app_label}.caregiverchildconsent')
        consent_onbehalf_objs = consent_onbehalf_cls.objects.filter(
            child_dob__lte=get_utcnow().date() - relativedelta(years=10),
            child_dob__gte=get_utcnow().date() - relativedelta(years=15, months=9),
            subject_consent__subject_identifier=visit.subject_identifier)
        return consent_onbehalf_objs
