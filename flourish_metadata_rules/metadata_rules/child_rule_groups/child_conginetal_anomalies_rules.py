from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P
from edc_constants.constants import YES

app_label = 'flourish_child'


@register()
class CongenitalAnomaliesRuleGroup(CrfRuleGroup):

    congenital_anomalies = CrfRule(
        predicate=P('congenital_anomalities', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantcongenitalanomalies']
    )

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.birthdata'
