from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

from ....predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class Covid19AdolRuleGroup(CrfRuleGroup):

    phq_screening_referral = CrfRule(
        predicate=pc.func_cough_and_fever,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.covid19adol',])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.tbvisitscreeningadolescent'
