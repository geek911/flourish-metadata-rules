from django.apps import apps as django_apps
from edc_base.utils import age, get_utcnow
from edc_constants.constants import FEMALE, YES
from edc_metadata_rules import PredicateCollection


class UrlMixinNoReverseMatch(Exception):
    pass


class ChildPredicates(PredicateCollection):

    app_label = 'flourish_child'
    pre_app_label = 'pre_flourish'
    maternal_app_label = 'flourish_caregiver'
    visit_model = f'{app_label}.childvisit'

    def mother_pregnant(self, visit=None, **kwargs):
        """Returns true if expecting
        """
        enrollment_model = django_apps.get_model(
            f'{self.maternal_app_label}.antenatalenrollment')
        try:
            enrollment_model.objects.get(subject_identifier=visit.subject_identifier[:-3])
        except enrollment_model.DoesNotExist:
            return False
        else:
            maternal_delivery_cls = django_apps.get_model(
                f'{self.maternal_app_label}.maternaldelivery')
            try:
                maternal_delivery_cls.objects.get(
                    subject_identifier=visit.subject_identifier[:-3])
            except maternal_delivery_cls.DoesNotExist:
                return True
        return False

    def get_child_age(self, visit=None, **kwargs):
        """Returns child age
        """
        if not self.mother_pregnant(visit=visit):
            caregiver_child_consent_cls = django_apps.get_model(
                f'{self.maternal_app_label}.caregiverchildconsent')
            try:
                caregiver_child_consent = caregiver_child_consent_cls.objects.get(
                    subject_identifier=visit.subject_identifier)
            except caregiver_child_consent_cls.DoesNotExist:
                return None
            else:
                return age(caregiver_child_consent.child_dob, get_utcnow())

    def child_age_at_enrolment(self, visit):
        if not self.mother_pregnant(visit=visit):
            dummy_consent_cls = django_apps.get_model(
                f'{self.app_label}.childdummysubjectconsent')
            try:
                dummy_consent = dummy_consent_cls.objects.get(
                    subject_identifier=visit.subject_identifier)
            except dummy_consent_cls.DoesNotExist:
                return None
            else:
                return dummy_consent.age_at_consent

    def func_consent_study_pregnant(self, visit=None, **kwargs):
        """Returns True if participant's mother consented to the study in pregnancy
        """
        maternal_delivery_cls = django_apps.get_model(
            f'{self.maternal_app_label}.maternaldelivery')
        try:
            maternal_delivery_cls.objects.get(subject_identifier=visit.subject_identifier[:-3],
                                              live_infants_to_register__gte=1)
        except maternal_delivery_cls.DoesNotExist:
            return False
        else:
            return True

    def func_specimen_storage_consent(self, visit=None, **kwargs):
        """Returns True if participant's mother consented to repository blood specimen
        storage at enrollment.
        """

        child_age = self.get_child_age(visit=visit)

        consent_cls = None
        subject_identifier = None

        if child_age < 7:
            consent_cls = django_apps.get_model(
                f'{self.maternal_app_label}.caregiverchildconsent')
            subject_identifier = visit.subject_ifdentifier[:-3]

        elif child_age >= 18:
            consent_cls = django_apps.get_model(f'{self.app_label}.childcontinuedconsent')
            subject_identifier = visit.subject_ifdentifier
        else:
            consent_cls = django_apps.get_model(f'{self.app_label}.childassent')
            subject_identifier = visit.subject_ifdentifier

        if consent_cls and subject_identifier:
            try:
                consent_obj = consent_cls.objects.get(
                    subject_identifier=subject_identifier)
            except consent_cls.DoesNotExist:
                return False
            else:
                return consent_obj.specimen_consent == YES

    def func_7_years_older(self, visit=None, **kwargs):
        """Returns true if participant is 7 years or older
        """
        child_age = self.get_child_age(visit=visit)
        return child_age.years >= 7 if child_age else False

    def func_12_years_older(self, visit=None, **kwargs):
        """Returns true if participant is 12 years or older
        """
        child_age = self.get_child_age(visit=visit)
        return child_age.years >= 12 if child_age else False

    def func_12_years_older_female(self, visit=None, **kwargs):
        """Returns true if participant is 12 years or older
        """
        assent_model = django_apps.get_model(f'{self.app_label}.childassent')
        try:
            assent_obj = assent_model.objects.get(subject_identifier=visit.subject_identifier)
        except assent_model.DoesNotExist:
            return False
        else:
            child_age = age(assent_obj.dob, get_utcnow())
            return child_age.years >= 12 and assent_obj.gender == FEMALE

    def func_2_months_older(self, visit=None, **kwargs):
        """Returns true if participant is 2 months or older
        """
        child_age = self.get_child_age(visit=visit)
        return child_age.months >= 2 if child_age else False

    def func_36_months_younger(self, visit=None, **kwargs):
        child_age = self.child_age_at_enrolment(visit=visit)
        return ((child_age.years * 12) + child_age.months) < 36 if child_age else False

    def func_continued_consent(self, visit=None, **kwargs):
        """Returns True if participant is over 18 and continued consent has been completed
        """
        continued_consent_cls = django_apps.get_model(
            f'{self.app_label}.childcontinuedconsent')
        try:
            continued_consent_cls.objects.get(subject_identifier=visit.subject_identifier)
        except continued_consent_cls.DoesNotExist:
            return False
        else:
            return True
