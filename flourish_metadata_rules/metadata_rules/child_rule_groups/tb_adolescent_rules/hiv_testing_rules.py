from edc_constants.constants import YES, NO
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

from ....predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class HIVTestingAdolRuleGroup(CrfRuleGroup):

    phq_screening_referral = CrfRule(
        predicate=P('tb_referral', 'eq', NO),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivtestingadol',])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.tbpresencehouseholdmembersadol'
