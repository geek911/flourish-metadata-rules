from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, PF

app_label = 'flourish_caregiver'


@register()
class EdinburgDeprScreeningRuleGroup(CrfRuleGroup):

    edinburg_screening_referral = CrfRule(
        predicate=PF('depression_score', 'self_harm',
                     func=lambda score, self_harm: True if score >= 10 or self_harm != '0' else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.caregiveredinburghreferral'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.caregiveredinburghdeprscreening'
