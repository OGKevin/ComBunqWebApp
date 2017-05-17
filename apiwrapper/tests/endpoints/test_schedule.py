import unittest

from apiwrapper.endpoints.schedule import Schedule
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ScheduleTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(Schedule)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account/%d/schedule" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_schedules_for_account(self):
        endpoint_should_be = "/user/%d/monetary-account/%d/schedule" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_schedules_for_account(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_schedule_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/schedule/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_schedule_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_schedules_for_user(self):
        endpoint_should_be = "/user/%d/schedule" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_schedules_for_user(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_instances_for_schedule(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/schedule/%d/schedule-instance" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_all_instances_for_schedule(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_schedule_instance_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/schedule/%d/schedule-instance/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_schedule_instance_by_id(
            self.random_id, self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
