from edc_constants.constants import YES, NO
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P, PF
from edc_constants.constants import POS
from ....predicates import ChildPredicates

app_label = 'flourish_child'


@register()
class TbVisitScreeningAdolRuleGroup(CrfRuleGroup):

    tb_referral_rule = CrfRule(
        predicate=PF('cough_duration', 'fever_duration', 'night_sweats',
                     'weight_loss', func=lambda cough, fever, sweats, weight_loss:
                     cough == YES or fever == True or sweats == True or weight_loss == True),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.tbreferaladol', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.tbvisitscreeningadolescent'
