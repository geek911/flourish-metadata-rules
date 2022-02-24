from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register

from flourish_labs import dna_pcr_panel, stool_sample_panel
from ....predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class ChildVisitReqRuleGroup(RequisitionRuleGroup):

    # Make VL Required regardless the pregnancy status
    dna_pcr_panel_rule = RequisitionRule(
        predicate=pc.func_hiv_exposed,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[dna_pcr_panel, stool_sample_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childvisit'
        requisition_model = f'{app_label}.childrequisition'
