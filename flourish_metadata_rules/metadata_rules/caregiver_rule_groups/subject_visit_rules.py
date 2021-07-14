from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from ...predicates import CaregiverPredicates

app_label = 'flourish_caregiver'
pc = CaregiverPredicates()


@register()
class MaternalVisitRuleGroup(CrfRuleGroup):

    preg_prior = CrfRule(
        predicate=pc.func_preg_no_prior_participation,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.foodsecurityquestionnaire',
                       f'{app_label}.ultrasound',
                       f'{app_label}.caregiveredinburghdeprscreening',
                       f'{app_label}.tbhistorypreg',
                       f'{app_label}.tbscreenpreg',
                       f'{app_label}.tbpresencehouseholdmembers'])

    biological_with_hiv_not_preg = CrfRule(
        predicate=pc.func_bio_mothers_hiv_not_preg,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivviralloadandcd4', ])

    biological_with_hiv = CrfRule(
        predicate=pc.func_bio_mothers_hiv,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.maternaldiagnoses',
                       f'{app_label}.maternalinterimidcc', ])

    biological_mother = CrfRule(
        predicate=pc.func_bio_mother,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.obstericalhistory',
                       f'{app_label}.caregiverclinicalmeasurements',
                       f'{app_label}.medicalhistory', ])

    # specimen_storage = CrfRule(
        # predicate=pc.func_specimen_storage_consent,
        # consequence=REQUIRED,
        # alternative=NOT_REQUIRED,
        # target_models=[f'{app_label}.bloodspecimenstorage', ])

    hiv_no_prior = CrfRule(
        predicate=pc.func_pregnant_hiv,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.arvsprepregnancy',
                       f'{app_label}.maternalarvduringpreg',
                       f'{app_label}.maternalhivinterimhx', ])

    non_preg = CrfRule(
        predicate=pc.func_non_pregnant_caregivers,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.caregiverphqdeprscreening'])

    LWHIV_10_15a = CrfRule(
        predicate=pc.func_LWHIV_aged_10_15a,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivdisclosurestatusa'])

    LWHIV_10_15b = CrfRule(
        predicate=pc.func_LWHIV_aged_10_15b,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivdisclosurestatusb', ])

    LWHIV_10_15c = CrfRule(
        predicate=pc.func_LWHIV_aged_10_15c,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivdisclosurestatusc', ])

    LWHIV_10_15d = CrfRule(
        predicate=pc.func_LWHIV_aged_10_15d,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivdisclosurestatusd', ])

    hiv_test = CrfRule(
        predicate=pc.func_show_hiv_test_form,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.hivrapidtestcounseling', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.maternalvisit'
