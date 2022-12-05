from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, PF, P


app_label = 'flourish_caregiver'


@register()
class TbInterviewRuleGroup(CrfRuleGroup):

    tb_transcription = CrfRule(
        predicate = P('interview_language', 'is not', None),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.tbinterviewtranscription'])

    tb_translation = CrfRule(
        predicate=P('interview_language', 'eq', 'setswana'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.tbinterviewtranslation'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.tbinterview'
