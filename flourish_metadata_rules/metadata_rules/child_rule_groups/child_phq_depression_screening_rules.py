from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from ...predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class ChildPHQ9DeprScreeningRuleGroup(CrfRuleGroup):

    phq_screening_referral = CrfRule(
        predicate=pc.func_phq9_referral_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childphqreferral'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childphqdepressionscreening'
