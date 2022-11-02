from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

from ...predicates import ChildPredicates
from flourish_metadata_rules import predicates

app_label = 'flourish_child'
pc = ChildPredicates()


@register()
class ChildVisitRuleGroup(CrfRuleGroup):

    birth_exam = CrfRule(
        predicate=P('is_present', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.birthexam', ])

    consent_study_pregnant = CrfRule(
        predicate=pc.func_consent_study_pregnant,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.birthdata', ])

    mother_pregnant_pos = CrfRule(
        predicate=pc.func_mother_preg_pos,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantarvexposure', ])

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
        predicate=pc.func_36_months_younger_not_birthvisit,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantfeeding', ])

    continued_consent_ready = CrfRule(
        predicate=pc.func_continued_consent,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childworkingstatus', ])

    age_3_months_old = CrfRule(
        predicate=pc.func_3_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening3months', ])

    age_6_months_old = CrfRule(
        predicate=pc.func_6_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening6months', ])

    age_9_months_old = CrfRule(
        predicate=pc.func_9_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening9months', ])

    age_12_months_old = CrfRule(
        predicate=pc.func_12_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening12months', ])

    age_18_months_old = CrfRule(
        predicate=pc.func_18_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening18months', ])

    age_36_months_old = CrfRule(
        predicate=pc.func_36_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening36months', ])

    age_60_months_old = CrfRule(
        predicate=pc.func_60_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening60months', ])

    age_72_months_old = CrfRule(
        predicate=pc.func_72_months_old,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantdevscreening72months', ])

    forth_eighth_quarter = CrfRule(
        predicate=pc.func_forth_eighth_quarter,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childfoodsecurityquestionnaire', ])
    
    birth_exam = CrfRule(
        predicate = P('is_present', 'eq', YES),
        consequence = REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.birthexam',])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childvisit'
