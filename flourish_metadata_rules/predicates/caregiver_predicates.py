from datetime import date
from flourish_caregiver.helper_classes import MaternalStatusHelper

from django.apps import apps as django_apps
from edc_base.utils import age
from edc_constants.constants import POS, YES, NEG
from edc_metadata_rules import PredicateCollection
from edc_reference.models import Reference


class CaregiverPredicates(PredicateCollection):
    app_label = 'flourish_caregiver'
    pre_app_label = 'pre_flourish'
    visit_model = f'{app_label}.maternalvisit'

    def func_hiv_positive(self, visit=None, **kwargs):
        """
        Get HIV Status from the rapid test results
        """
        maternal_status_helper = MaternalStatusHelper(
            maternal_visit=visit, subject_identifier=visit.subject_identifier)
        return maternal_status_helper.hiv_status == POS

    def viral_load(self, visit=None, **kwargs):
        """
        Returns true if the visit is 1000 or 200D and the caregiver is pos
        """
        return self.func_hiv_positive(visit=visit) and visit.visit_code in ['1000M',
                                                                            '2000D']

    def enrolled_pregnant(self, visit=None, **kwargs):
        """Returns true if expecting
        """
        enrollment_model = django_apps.get_model(f'{self.app_label}.antenatalenrollment')
        try:
            enrollment_model.objects.get(subject_identifier=visit.subject_identifier)
        except enrollment_model.DoesNotExist:
            return False
        else:
            return True

    def currently_pregnant(self, visit=None, **kwargs):

        if self.enrolled_pregnant(visit=visit, **kwargs):
            maternal_delivery_cls = django_apps.get_model(
                f'{self.app_label}.maternaldelivery')
            try:
                maternal_delivery_cls.objects.get(
                    subject_identifier=visit.subject_identifier)
            except maternal_delivery_cls.DoesNotExist:
                return True
        return False

    def is_child_offstudy(self, child_subject_identifier):

        offstudy_cls = django_apps.get_model('flourish_prn.childoffstudy')

        try:
            offstudy_cls.objects.get(subject_identifier=child_subject_identifier)
        except offstudy_cls.DoesNotExist:
            return False
        else:
            return True

    def child_gt10(self, visit):

        onschedule_model = django_apps.get_model(
            visit.appointment.schedule.onschedule_model)
        child_subject_identifier = None

        try:
            onschedule_obj = onschedule_model.objects.get(
                subject_identifier=visit.appointment.subject_identifier,
                schedule_name=visit.appointment.schedule_name)
        except onschedule_model.DoesNotExist:
            pass
        else:

            if 'antenatal' not in onschedule_obj.schedule_name:
                child_subject_identifier = onschedule_obj.child_subject_identifier

        if child_subject_identifier and not self.is_child_offstudy(
                child_subject_identifier):
            registered_model = django_apps.get_model(
                f'edc_registration.registeredsubject')

            try:
                registered_child = registered_model.objects.get(
                    subject_identifier=child_subject_identifier)
            except registered_model.DoesNotExist:
                raise
            else:
                child_age = age(registered_child.dob, visit.report_datetime)
                child_age = float(f'{child_age.years}.{child_age.months}')

                if (child_age <= 15.9 and child_age >= 10):
                    return [True, child_subject_identifier]
        return [False, child_subject_identifier]

    def prior_participation(self, visit=None, **kwargs):
        maternal_dataset_model = django_apps.get_model(
            f'{self.app_label}.maternaldataset')

        try:
            maternal_dataset_model.objects.get(
                subject_identifier=visit.subject_identifier)
        except maternal_dataset_model.DoesNotExist:
            return False
        else:
            return True

    def func_preg_no_prior_participation(self, visit=None, **kwargs):
        """Returns true if participant is expecting and never
        participated in a BHP study for enrollment_visit.
        """
        return (self.enrolled_pregnant(visit=visit)
                and not self.prior_participation(visit=visit))

    def func_caregiver_no_prior_participation(self, visit=None, **kwargs):
        """Returns true if participant is a caregiver and never participated in a BHP study.
        """
        return (not self.enrolled_pregnant(visit=visit)
                and not self.prior_participation(visit=visit))

    def func_bio_mother(self, visit=None, **kwargs):
        consent_cls = django_apps.get_model(f'{self.app_label}.subjectconsent')

        consent_obj = consent_cls.objects.filter(
            subject_identifier=visit.subject_identifier,).latest('created')

        return consent_obj.biological_caregiver == YES

    def func_bio_mother_hiv(self, visit=None, maternal_status_helper=None, **kwargs):
        """Returns true if participant is non-pregnant biological mother living with HIV.
        """
        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        return (self.func_bio_mother(visit=visit) and not self.currently_pregnant(
            visit=visit)
                and maternal_status_helper.hiv_status == POS)

    def func_bio_mothers_hiv_cohort_a(self, visit=None, maternal_status_helper=None, **kwargs):
        """Returns true if participant is biological mother living with HIV.
        """

        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        cohort_a = visit.schedule_name[:2] == 'a_'

        return cohort_a and self.func_bio_mother_hiv(visit=visit)

    def func_pregnant_hiv(self, visit=None, maternal_status_helper=None, **kwargs):
        """Returns true if a newly enrolled participant is pregnant and living with HIV.
        """
        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        return (self.enrolled_pregnant(visit=visit)
                and maternal_status_helper.hiv_status == POS)

    def func_non_pregnant_caregivers(self, visit=None, **kwargs):
        """Returns true if non pregnant.
        """
        return not self.enrolled_pregnant(visit=visit)

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

    def child_gt10_eligible(self, visit, maternal_status_helper, id_post_fix):

        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            maternal_visit=visit)

        gt_10, child_subject_identifier = self.child_gt10(visit)

        if child_subject_identifier:
            child_exists = child_subject_identifier[-3:] in id_post_fix

            return maternal_status_helper.hiv_status == POS and gt_10 and child_exists
        return False

    def func_LWHIV_aged_10_15a(self, visit=None, maternal_status_helper=None, **kwargs):

        values = self.exists(
            reference_name=f'{self.app_label}.hivdisclosurestatusa',
            subject_identifier=visit.subject_identifier,
            field_name='disclosed_status',
            value=YES)

        return len(values) == 0 and self.child_gt10_eligible(
            visit, maternal_status_helper,
            ['-10', '-60', '-70', '-80', '-25', '-36'])

    def func_LWHIV_aged_10_15b(self, visit=None, maternal_status_helper=None, **kwargs):

        values = self.exists(
            reference_name=f'{self.app_label}.hivdisclosurestatusb',
            subject_identifier=visit.subject_identifier,
            field_name='disclosed_status',
            value=YES)

        return len(values) == 0 and self.child_gt10_eligible(visit,
                                                             maternal_status_helper,
                                                             ['-25', ])

    def func_LWHIV_aged_10_15c(self, visit=None, maternal_status_helper=None, **kwargs):

        values = self.exists(
            reference_name=f'{self.app_label}.hivdisclosurestatusc',
            subject_identifier=visit.subject_identifier,
            field_name='disclosed_status',
            value=YES)

        return len(values) == 0 and self.child_gt10_eligible(visit,
                                                             maternal_status_helper,
                                                             ['-36', ])

    def func_show_hiv_test_form(
            self, visit=None, maternal_status_helper=None, **kwargs
            ):
        subject_identifier = visit.subject_identifier
        result_date = None

        maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
            visit)

        if maternal_status_helper.hiv_status != POS:
            if self.currently_pregnant(visit=visit) and visit.visit_code == '1000M':
                return True
            elif (maternal_status_helper.hiv_status == NEG
                  and not self.currently_pregnant(visit=visit)
                  and visit.visit_code == '2000M'):
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

                    if result_date and isinstance(result_date[0], date):
                        return (visit.report_datetime.date() - result_date[0]).days > 90
        return False
