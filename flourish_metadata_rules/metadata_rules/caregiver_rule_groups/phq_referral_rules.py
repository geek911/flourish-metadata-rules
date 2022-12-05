from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P
from ...predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class PHQ9ReferralRuleGroup(CrfRuleGroup):

    phq_referral_fu = CrfRule(
        predicate=P('referred_to', 'eq', 'receiving_emotional_care'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.caregiverphqreferralfu'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.caregiverphqreferral'
