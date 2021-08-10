from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
from edc_constants.constants import POS, YES, NEG
from edc_metadata_rules import PredicateCollection
from edc_reference.models import Reference
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

    def onstudy_children_count_gt10(self, visit):

        registered_cls = django_apps.get_model(f'edc_registration.registeredsubject')
        child_offstudy_cls = django_apps.get_model(f'flourish_prn.childoffstudy')

        offstudy_child_ids = child_offstudy_cls.objects.filter(
            subject_identifier__startswith=visit.subject_identifier)

        registered_child_objs = registered_cls.objects.filter(
            subject_identifier__startswith=visit.subject_identifier,
            dob__lte=get_utcnow().date() - relativedelta(years=10),
            dob__gte=get_utcnow().date() - relativedelta(years=15, months=9)).exclude(
            subject_identifier__in=offstudy_child_ids)

        return registered_child_objs.count()

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

        return (self.func_bio_mother(visit=visit)
                and maternal_status_helper.hiv_status == POS)

    def func_bio_mothers_hiv_not_preg(self, visit=None,
                                      maternal_status_helper=None, **kwargs):
        """Returns true if participant is biological mother living with HIV.
        """
        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        return (not self.pregnant(visit=visit)
                and (self.func_bio_mothers_hiv(visit=visit)))

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

    def func_LWHIV_aged_10_15a(self, visit=None, **kwargs):

        return self.onstudy_children_count_gt10(visit=visit) >= 1

    def func_LWHIV_aged_10_15b(self, visit=None, **kwargs):
        return self.onstudy_children_count_gt10(visit=visit) >= 2

    def func_LWHIV_aged_10_15c(self, visit=None, **kwargs):

        return self.onstudy_children_count_gt10(visit=visit) >= 3

    def func_LWHIV_aged_10_15d(self, visit=None, **kwargs):
        return self.onstudy_children_count_gt10(visit=visit) == 4

    def func_show_hiv_test_form(
            self, visit=None, maternal_status_helper=None, **kwargs):
        subject_identifier = visit.subject_identifier
        result_date = None

        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            visit)

        if maternal_status_helper.hiv_status != POS:
            if self.pregnant(visit=visit) and visit.visit_code == '1000M':
                return True
            elif (maternal_status_helper.hiv_status == NEG
                    and not self.pregnant(visit=visit) and visit.visit_code == '2000M'):
                return True
            else:
                prev_rapid_test = Reference.objects.filter(
                    model=f'{self.app_label}.hivrapidtestcounseling',
                    report_datetime__lt=visit.report_datetime,
                    identifier=subject_identifier).order_by(
                        '-report_datetime').last()

                if prev_rapid_test:
                    result_date = self.exists(
                                reference_name=f'{self.app_label}.hivrapidtestcounseling',
                                subject_identifier=visit.subject_identifier,
                                report_datetime=prev_rapid_test.report_datetime,
                                field_name='result_date')

                    result_date = self.refsets(
                        reference_name=f'{self.app_label}.hivrapidtestcounseling',
                        subject_identifier=visit.subject_identifier,
                        report_datetime=prev_rapid_test.report_datetime).fieldset(
                        field_name='result_date').all().values

                    return (visit.report_datetime.date() - result_date[0]).days > 90
        return False
