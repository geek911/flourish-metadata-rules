from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

app_label = 'flourish_child'


@register()
class ChildSocioDemographicRuleGroup(CrfRuleGroup):

    gad_anxiety_referral = CrfRule(
        predicate=P('attend_school', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.academicperformance'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childsociodemographic'
