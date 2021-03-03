from django.apps import apps as django_apps
from edc_constants.constants import POS, IND, YES
from edc_metadata_rules import PredicateCollection
from flourish_caregiver.helper_classes import Cohort

class CaregiverPredicates(PredicateCollection):
    
    app_label = 'flourish_caregiver'
    pre_app_label = 'pre_flourish'
    visit_model = f'{app_label}.maternalvisit'

    def hiv_status(self, visit=None):

        rapid_test_model = django_apps.get_model(f'{self.app_label}.hivrapidtestcounseling')

        try:
            rapid_test_obj = rapid_test_model.objects.get(maternal_visit__subject_identifier=visit.subject_identifier)
        except rapid_test_model.DoesNotExist:

            prior_participation = self.prior_participation(visit=visit)
            if prior_participation:
                return prior_participation.mom_hivstatus
            else:
                enrollment_model = django_apps.get_model(f'{self.app_label}.antenatalenrollment')
                try:
                    enrollment_obj = enrollment_model.objects.get(
                                                subject_identifier=visit.subject_identifier)
                except enrollment_model.DoesNotExist:
                    return IND
                else:
                    return enrollment_obj.current_hiv_status
        else:
            return rapid_test_obj.result

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
                maternal_delivery_obj = maternal_delivery_cls.objects.get(
                                        subject_identifier=visit.subject_identifier)
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

    def func_bio_mothers_hiv(self, visit=None, **kwargs):
        """Returns true if participant is biological mother living with HIV.
        """
        if self.pregnant(visit=visit):
            return self.hiv_status(visit=visit) == POS
        else:
            cyhuu_model = django_apps.get_model(f'{self.pre_app_label}.cyhuupreenrollment')

            try:
                cyhuu_obj = cyhuu_model.objects.get(maternal_visit__appointment__subject_identifier=visit.subject_identifier)
            except cyhuu_model.DoesNotExist:
                return False
            else:
                return cyhuu_obj.biological_mother == YES and self.hiv_status(visit=visit) == POS

    def func_pregnant_hiv(self, visit=None, **kwargs):
        """Returns true if a newly enrolled participant is pregnant and living with HIV.
        """ 
        return self.pregnant(visit=visit) and self.hiv_status(visit=visit) == POS

    def func_non_pregnant_caregivers(self, visit=None, **kwargs):
        """Returns true if non pregnant.
        """
        return not self.pregnant(visit=visit)
