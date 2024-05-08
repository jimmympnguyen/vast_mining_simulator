import unittest

from mining_simulator.unloading_station import UnloadStation
from mining_simulator.mining_truck import MiningTruck


class TestMiningStation(unittest.TestCase):
    def setUp(self):
        self.unload_station1 = UnloadStation()
        self.unload_station2 = UnloadStation()
        self.mining_truck1 = MiningTruck()
        self.mining_truck2 = MiningTruck()

    def test_current_wait_time_zero(self):
        result = min(self.unload_station1, self.unload_station2)
        self.assertTrue(result.id == self.unload_station1.id)

    def test_current_wait_time_station1(self):
        self.unload_station1.current_wait_time = 0
        self.unload_station2.current_wait_time = 10
        result = min(self.unload_station1, self.unload_station2)
        self.assertTrue(result.id == self.unload_station1.id)

    def test_current_wait_time_station2(self):
        self.unload_station1.current_wait_time = 5
        self.unload_station2.current_wait_time = 0
        result = min(self.unload_station1, self.unload_station2)
        self.assertTrue(result.id == self.unload_station2.id)

    def test_add_truck_to_empty_queue(self):
        self.unload_station1.add_truck_to_queue(self.mining_truck1)
        self.assertTrue(
            self.mining_truck1.current_action == self.mining_truck1.Actions.UNLOADING
        )
        self.assertTrue(
            self.unload_station1.current_wait_time == self.mining_truck1.timer
        )
        self.assertTrue(len(self.unload_station1.queue) == 1)

    def test_add_two_trucks_to_queue(self):
        self.unload_station1.add_truck_to_queue(self.mining_truck1)
        self.assertTrue(
            self.unload_station1.current_wait_time == self.mining_truck1.timer
        )

        self.unload_station1.add_truck_to_queue(self.mining_truck2)
        self.assertTrue(
            self.mining_truck1.current_action == self.mining_truck1.Actions.UNLOADING
        )
        self.assertTrue(
            self.mining_truck2.current_action == self.mining_truck2.Actions.WAITING
        )
        self.assertTrue(
            self.unload_station1.current_wait_time
            == self.mining_truck1.timer + self.mining_truck2.timer
        )
        self.assertTrue(len(self.unload_station1.queue) == 2)

    def test_manage_queue(self):
        self.unload_station1.add_truck_to_queue(self.mining_truck1)
        self.unload_station1.add_truck_to_queue(self.mining_truck2)

        self.unload_station1.manage_queue()
        self.assertTrue(
            self.mining_truck2.current_action == self.mining_truck2.Actions.WAITING
        )
        self.assertTrue(self.unload_station1.total_wait_time == 5)

        self.mining_truck1.timer = 0
        self.unload_station1.manage_queue()
        self.assertTrue(
            self.mining_truck2.current_action == self.mining_truck2.Actions.UNLOADING
        )
        self.assertTrue(self.mining_truck1.units_mined == 1)
        self.assertTrue(self.unload_station1.units_deposited == 1)
        self.assertTrue(len(self.unload_station1.queue) == 1)
        self.assertTrue(self.unload_station1.total_wait_time == 10)

        self.mining_truck2.timer = 0
        self.unload_station1.manage_queue()
        self.assertTrue(self.mining_truck1.units_mined == 1)
        self.assertTrue(self.mining_truck2.units_mined == 1)
        self.assertTrue(self.unload_station1.units_deposited == 2)
        self.assertTrue(len(self.unload_station1.queue) == 0)
        self.assertTrue(self.unload_station1.total_wait_time == 10)
