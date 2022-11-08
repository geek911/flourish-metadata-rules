from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from ...predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class EdinburgDeprScreeningRuleGroup(CrfRuleGroup):

    edinburg_screening_referral = CrfRule(
        predicate=pc.func_edinburgh_referral_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.caregiveredinburghreferral'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.caregiveredinburghdeprscreening'
