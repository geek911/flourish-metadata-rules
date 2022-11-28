from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, PF

from ...predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class ChildPHQ9DeprScreeningRuleGroup(CrfRuleGroup):

    phq_screening_referral = CrfRule(
        predicate=PF('depression_score', 'self_harm', 'self_harm_thoughts',
                     'suidice_attempt',
                     func=lambda w, x, y, z: True if w >= 10 or x != '0' or y == YES or z == YES else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childphqreferral'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childphqdepressionscreening'
