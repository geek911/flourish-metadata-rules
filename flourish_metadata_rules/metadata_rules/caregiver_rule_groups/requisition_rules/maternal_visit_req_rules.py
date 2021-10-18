from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register

from flourish_labs.caregiver_panels import viral_load_panel
from ....predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class MaternalVisitReqRuleGroup(RequisitionRuleGroup):

    viral_load_panel = RequisitionRule(
        predicate=pc.func_pregnant_hiv,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[viral_load_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.maternalvisit'
        requisition_model = f'{app_label}.caregiverrequisition'
