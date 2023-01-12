from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P, PF
from ...predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class EdinburgReferralRuleGroup(CrfRuleGroup):

    edinburg_referral_fu = CrfRule(
        predicate=P('referred_to', 'eq', 'receiving_emotional_care'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.caregiveredinburghreferralfu'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.caregiveredinburghreferral'
