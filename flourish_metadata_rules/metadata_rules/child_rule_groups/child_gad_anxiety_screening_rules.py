from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

app_label = 'flourish_child'


@register()
class ChildGAD7AnxietyScreeningRuleGroup(CrfRuleGroup):

    gad_anxiety_referral = CrfRule(
        predicate=P('anxiety_score', 'gte', 10),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childgadreferral'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childgadanxietyscreening'
