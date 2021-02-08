from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.tests import SiteTestCaseMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, POS
from edc_facility.import_holidays import import_holidays
from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from .models import MaternalDataset, AntenatalEnrollment, CyhuuPreEnrollment
from .models import HivRapidTestCounseling, MaternalVisit, Appointment
from ..predicates import CaregiverPredicates

class TestMaternalPredicates(SiteTestCaseMixin, TestCase):

    reference_helper_cls = ReferenceTestHelper
    app_label = 'flourish_metadata_rules'
    visit_model = 'flourish_caregiver.maternalvisit'
    reference_model = 'edc_reference.reference'

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def tearDown(self):
        super().tearDown()

    def setUp(self):

        self.subject_identifier = '111111111'
        self.reference_helper = self.reference_helper_cls(
            visit_model=self.visit_model,
            subject_identifier=self.subject_identifier)

        report_datetime = get_utcnow()
        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='1000M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=1),
            timepoint='2000M')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint='3000M')
        import_holidays()

    def test_func_preg_no_prior_participation(self):
        pc = CaregiverPredicates()
        pc.app_label = self.app_label

        AntenatalEnrollment.objects.create(subject_identifier=self.subject_identifier)

        self.assertTrue(
            pc.func_preg_no_prior_participation(self.maternal_visits[0],))

    def test_func_caregiver_no_prior_participation(self):
        pc = CaregiverPredicates()
        pc.app_label = self.app_label

        self.assertTrue(
            pc.func_caregiver_no_prior_participation(self.maternal_visits[0],))

    def test_func_bio_mothers_hiv(self):
        pc = CaregiverPredicates()
        pc.app_label = self.app_label
        pc.pre_app_label = self.app_label

        MaternalDataset.objects.create(subject_identifier=self.subject_identifier)
        appointment = Appointment.objects.create(subject_identifier=self.subject_identifier)
        maternal_visit = MaternalVisit.objects.create(appointment=appointment,
                                                      subject_identifier=self.subject_identifier)
        CyhuuPreEnrollment.objects.create(maternal_visit=maternal_visit,
                                          biological_mother=YES)
        HivRapidTestCounseling.objects.create(maternal_visit=maternal_visit,
                                              subject_identifier=self.subject_identifier,
                                              result=POS)

        self.assertTrue(
            pc.func_bio_mothers_hiv(self.maternal_visits[0],))

    def test_func_pregnant_hiv(self):
        pc = CaregiverPredicates()
        pc.app_label = self.app_label

        MaternalDataset.objects.create(subject_identifier=self.subject_identifier)
        AntenatalEnrollment.objects.create(subject_identifier=self.subject_identifier)
        appointment = Appointment.objects.create(subject_identifier=self.subject_identifier)
        maternal_visit = MaternalVisit.objects.create(appointment=appointment,
                                                      subject_identifier=self.subject_identifier)
        HivRapidTestCounseling.objects.create(maternal_visit=maternal_visit,
                                              subject_identifier=self.subject_identifier,
                                              result=POS)

        self.assertTrue(
            pc.func_pregnant_hiv(self.maternal_visits[0],))

    def test_func_non_pregnant_caregivers(self):
        pc = CaregiverPredicates()
        pc.app_label = self.app_label

        MaternalDataset.objects.create(subject_identifier=self.subject_identifier)
        self.assertTrue(
            pc.func_non_pregnant_caregivers(self.maternal_visits[0],))

    @property
    def maternal_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')
