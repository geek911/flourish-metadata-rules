from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P, PF
from ...predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class PHQ9DeprScreeningRuleGroup(CrfRuleGroup):

    phq_screening_referral = CrfRule(
        predicate=PF('depression_score', 'self_harm',
                     func=lambda score, self_harm: True if score >= 5 or self_harm != '0'
                     else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.caregiverphqreferral'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.caregiverphqdeprscreening'
