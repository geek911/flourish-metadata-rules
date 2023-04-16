from edc_constants.constants import YES, NO
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P, PF
from edc_constants.constants import POS
from ....predicates import ChildPredicates

app_label = 'flourish_child'


@register()
class TbLabResultsAdolRuleGroup(CrfRuleGroup):

    tb_referral_rule = CrfRule(
        predicate=P('quantiferon_result', 'eq', POS),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.tbreferaladol', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.tblabresultsadol'
