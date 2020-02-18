from mock import patch, MagicMock
# adapted from: https://stackoverflow.com/questions/8658043/how-to-mock-an-import
import sys
inst_mock = MagicMock()
sys.modules['inst'] = inst_mock
from emuloop import inclusive_float_range_with_step_flip, DoRun
import unittest


class TestRange(unittest.TestCase):

    def test_GIVEN_float_range_WHEN_get_range_THEN_inclusive_AND_expected_values(self):
        # GIVEN float range
        start, stop, step = 0.5, 2, 0.5
        # WHEN get range
        returned_range = []
        for i in inclusive_float_range_with_step_flip(start, stop, step):
            returned_range.append(i)
        # THEN inclusive AND expected values
        self.assertEqual([0.5, 1, 1.5, 2], returned_range)

    def test_GIVEN_inverted_float_range_WHEN_get_range_THEN_inclusive_AND_expected_values(self):
        # GIVEN float range
        start, stop, step = 2, 0.5, 0.5
        # WHEN get range
        returned_range = []
        for i in inclusive_float_range_with_step_flip(start, stop, step):
            returned_range.append(i)
        # THEN inclusive AND expected values
        self.assertEqual([2, 1.5, 1, 0.5], returned_range)


class TestRun(unittest.TestCase):

    def setUp(self):
        self.script_definition = DoRun()
        self.script_definition.begin_waitfor_mevents_end = MagicMock()
        inst_mock.reset_mock()

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_both_temp_field_scans_WHEN_run_THEN_scans_run_once_for_each_set(self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="10.0", step_temperature="1",
                                   start_field="2.0", stop_field="20.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="LF")
        inst_mock.lf0.assert_called_once()
        self.assertEqual(inst_mock.settemp.call_count, 10)
        self.assertEqual(inst_mock.setmag.call_count, 10 * 10)
        self.assertEqual(self.script_definition.begin_waitfor_mevents_end.call_count, 10 * 10)

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_temp_scan_field_point_WHEN_run_THEN_setmag_called_once_AND_scan_runs(self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="10.0", step_temperature="1",
                                   start_field="2.0", stop_field="2.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="LF")
        inst_mock.lf0.assert_called_once()
        self.assertEqual(inst_mock.settemp.call_count, 10)
        inst_mock.setmag.assert_called_once()
        self.assertEqual(self.script_definition.begin_waitfor_mevents_end.call_count, 10)

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_field_scan_temp_point_WHEN_run_THEN_settemp_called_once_AND_scan_runs(self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="1.0", step_temperature="1",
                                   start_field="2.0", stop_field="20.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_called_once()
        inst_mock.settemp.assert_called_once()
        self.assertEqual(inst_mock.setmag.call_count, 10)
        self.assertEqual(self.script_definition.begin_waitfor_mevents_end.call_count, 10)

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_both_field_and_temp_points_WHEN_run_THEN_temp_mag_run_called_once(self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="1.0", step_temperature="1",
                                   start_field="2.0", stop_field="2.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_called_once()
        inst_mock.settemp.assert_called_once()
        inst_mock.setmag.assert_called_once()
        self.script_definition.begin_waitfor_mevents_end.assert_called_once()

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_one_of_start_stop_field_is_keep_AND_temp_scan_WHEN_run_THEN_setmag_not_called_AND_temp_scans_run(
            self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="10.0", step_temperature="1",
                                   start_field="keep", stop_field="10.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_not_called()
        self.assertEqual(inst_mock.settemp.call_count, 10)
        inst_mock.setmag.assert_not_called()
        self.assertEqual(self.script_definition.begin_waitfor_mevents_end.call_count, 10)

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_one_of_start_stop_field_is_keep_AND_temp_point_WHEN_run_THEN_setmag_not_called_AND_temp_set(self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="1.0", step_temperature="1",
                                   start_field="keep", stop_field="keep", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_not_called()
        inst_mock.settemp.assert_called_once()
        inst_mock.setmag.assert_not_called()
        self.script_definition.begin_waitfor_mevents_end.assert_called_once()

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_one_of_start_stop_temp_is_keep_AND_field_scan_WHEN_run_THEN_settemp_not_called_AND_field_scans_run(
            self, _):
        self.script_definition.run(start_temperature="1.0", stop_temperature="keep", step_temperature="1",
                                   start_field="2", stop_field="20.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_called_once()
        self.assertEqual(inst_mock.setmag.call_count, 10)
        inst_mock.settemp.assert_not_called()
        self.assertEqual(self.script_definition.begin_waitfor_mevents_end.call_count, 10)

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_one_of_start_stop_temp_is_keep_AND_field_point_WHEN_run_THEN_settemp_not_called_AND_mag_set(self, _):
        self.script_definition.run(start_temperature="keep", stop_temperature="1.0", step_temperature="1",
                                   start_field="2", stop_field="2.0", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_called_once()
        inst_mock.setmag.assert_called_once()
        inst_mock.settemp.assert_not_called()
        self.script_definition.begin_waitfor_mevents_end.assert_called_once()

    @patch('genie_python.genie.cget', return_value={"value": "A Magnet"})
    def test_GIVEN_keep_temp_and_field_WHEN_run_THEN_settemp_and_setmag_not_called_AND_begin_waitfor_called_once(
            self, _):
        self.script_definition.run(start_temperature="keep", stop_temperature="1.0", step_temperature="1",
                                   start_field="2", stop_field="keep", step_field="2.0",
                                   custom="None", mevents="10", magnet_device="TF")
        inst_mock.tf0.assert_not_called()
        inst_mock.setmag.assert_not_called()
        inst_mock.settemp.assert_not_called()
        self.script_definition.begin_waitfor_mevents_end.assert_called_once()
