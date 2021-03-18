from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, P, register
from ...predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class ChildVisitRuleGroup(CrfRuleGroup):

    consent_study_pregnan = CrfRule(
        predicate=pc.func_consent_study_pregnant,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.birth_data',
                       f'{app_label}.infantarvexposure', ])

#     older_than_7 = CrfRule(
#         predicate=pc.func_7_years_older,
#         consequence=REQUIRED,
#         alternative=NOT_REQUIRED,
#         target_models=[f'{app_label}.tannerstaging',])

#     female_older_12 = CrfRule(
#         predicate=pc.func_12_years_older_female,
#         consequence=REQUIRED,
#         alternative=NOT_REQUIRED,
#         target_models=[f'{app_label}.pregnancy'])

    older_than_12 = CrfRule(
        predicate=pc.func_12_years_older,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childphqdepressionscreening',
                       f'{app_label}.childgadanxietyscreening'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.maternalvisit'
