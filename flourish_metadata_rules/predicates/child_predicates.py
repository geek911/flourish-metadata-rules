from edc_metadata_rules import PredicateCollection
from edc_base.utils import age, get_utcnow
from edc_constants.constants import FEMALE


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
        enrollment_model = django_apps.get_model(f'{self.maternal_app_label}.antenatalenrollment')
        try:
            enrollment_model.objects.get(subject_identifier=visit.subject_identifier[:-3])
        except enrollment_model.DoesNotExist:
            return False
        else:
            maternal_delivery_cls = django_apps.get_model(f'{self.maternal_app_label}.maternaldelivery')
            try:
                maternal_delivery_obj = maternal_delivery_cls.objects.get(
                                        subject_identifier=visit.subject_identifier)
            except maternal_delivery_cls.DoesNotExist:
                return True
        return False

    def get_child_age(self, visit=None, **kwargs):
        """Returns child age
        """
        assent_model = django_apps.get_model(f'{self.app_label}.childassent')
        try:
            assent_obj = assent_model.objects.get(subject_identifier=visit.subject_identifier)
        except assent_model.DoesNotExist:
            return None
        else:
            return age(assent_obj.dob, get_utcnow)
    
    def func_7_years_older(self, visit=None, **kwargs):
        """Returns true if participant is 7 years or older
        """
        child_age = self.get_child_age():
        return child_age.years >= 7 if child_age else False
        
    def func_12_years_older(self, visit=None, **kwargs):
        """Returns true if participant is 12 years or older
        """
        child_age = self.get_child_age():
        return child_age.years >= 12 if child_age else False
    
    def func_12_years_older_female(self, visit=None, **kwargs):
        """Returns true if participant is 12 years or older
        """
        child_dataset_model = django_apps.get_model(f'{self.app_label}.childdataset')
        try:
            child_dataset_obj = child_dataset_model.objects.get(subject_identifier=visit.subject_identifier)
        except child_dataset_model.DoesNotExist:
            return None
        
        child_age = self.get_child_age():
        if child_age:
            return child_age.years >= 12 and child_dataset_obj.infant_sex == FEMALE
        return False
    
    def func_2_years_older(self, visit=None, **kwargs):
        """Returns true if participant is 2 months or older
        """
        child_age = self.get_child_age():
        return child_age.months >= 2 if child_age else False

    