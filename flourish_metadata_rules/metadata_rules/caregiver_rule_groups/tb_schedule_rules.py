from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from flourish_metadata_rules.predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class TbScheduleRuleGroup(CrfRuleGroup):
    tb_off_schedule = CrfRule(
        predicate=pc.tb_off_schedule,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.tboffstudy', ])


    class Meta:
        app_label = app_label
        source_model = f'{app_label}.tbvisitscreeningwomen'
