import unittest

from mining_simulator.mining_site import MiningSite
from mining_simulator.unloading_station import UnloadStation
from mining_simulator.mining_truck import MiningTruck


class TestMiningStation(unittest.TestCase):
    def setUp(self):
        self.mining_site = MiningSite()
        self.mining_truck = MiningTruck()
        self.unload_station = UnloadStation()

    def test_next_action_travel_to_unload(self):
        self.mining_truck.timer = 0
        self.mining_truck.current_action = self.mining_truck.Actions.MINING
        self.mining_truck.take_action()
        self.assertTrue(
            self.mining_truck.current_action
            == self.mining_truck.Actions.TRAVEL_TO_UNLOAD
        )
        self.assertTrue(self.mining_truck.time_mining == 5)
        self.assertTrue(self.mining_truck.time_travelling == 0)

    def test_next_action_travel_to_mine(self):
        self.mining_truck.timer = 0
        self.mining_truck.current_action = self.mining_truck.Actions.UNLOADING
        self.mining_truck.take_action()
        self.assertTrue(
            self.mining_truck.current_action == self.mining_truck.Actions.TRAVEL_TO_MINE
        )
        self.assertTrue(self.mining_truck.time_unloading == 5)
        self.assertTrue(self.mining_truck.time_travelling == 0)

    def test_next_action_mining(self):
        self.mining_truck.sim_step_time_minutes = 5
        self.mining_truck.timer = 0
        self.mining_truck.current_action = self.mining_truck.Actions.TRAVEL_TO_MINE

        self.mining_truck.take_action()
        self.assertTrue(
            self.mining_truck.current_action == self.mining_truck.Actions.MINING
        )
        self.assertTrue(self.mining_truck.time_travelling == 5)
        self.assertTrue(self.mining_truck.time_mining == 0)

    def test_next_action_unloading(self):
        self.mining_truck.sim_step_time_minutes = 5
        self.mining_truck.timer = 0
        self.mining_truck.current_action = self.mining_truck.Actions.TRAVEL_TO_UNLOAD

        self.mining_truck.take_action()
        self.assertTrue(
            self.mining_truck.current_action == self.mining_truck.Actions.UNLOADING
        )
        self.assertTrue(self.mining_truck.time_travelling == 5)
        self.assertTrue(self.mining_truck.time_unloading == 0)

    def test_same_state(self):
        self.mining_truck.sim_step_time_minutes = 5
        self.mining_truck.timer = 10
        self.mining_truck.current_action = self.mining_truck.Actions.MINING
        self.mining_truck.take_action()
        self.assertTrue(
            self.mining_truck.current_action == self.mining_truck.Actions.MINING
        )
        self.assertTrue(self.mining_truck.time_mining == 5)
        self.assertTrue(self.mining_truck.timer == 5)

        self.mining_truck.take_action()
        self.mining_truck.sim_step_time_minutes = 5
        self.assertTrue(
            self.mining_truck.current_action == self.mining_truck.Actions.MINING
        )
        self.assertTrue(self.mining_truck.time_mining == 10)
        self.assertTrue(self.mining_truck.timer == 0)
