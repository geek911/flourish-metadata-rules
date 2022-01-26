from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from ...predicates import ChildPredicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class ChildVisitRuleGroup(CrfRuleGroup):

    consent_study_pregnant = CrfRule(
        predicate=pc.func_consent_study_pregnant,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.birthdata',
                       f'{app_label}.infantarvexposure', ])

    older_than_7 = CrfRule(
        predicate=pc.func_7_years_older,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childtannerstaging', ])

    female_older_12 = CrfRule(
        predicate=pc.func_12_years_older_female,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childpregtesting'])

    older_than_12 = CrfRule(
        predicate=pc.func_12_years_older,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childphqdepressionscreening',
                       f'{app_label}.childgadanxietyscreening'])

    younger_than_36months = CrfRule(
        predicate=pc.func_36_months_younger,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantfeeding', ])

    older_than_36months = CrfRule(
        predicate=pc.func_36_months_younger,
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_models=[f'{app_label}.childfoodsecurityquestionnaire', ])

    continued_consent_ready = CrfRule(
        predicate=pc.func_continued_consent,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childworkingstatus', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childvisit'
