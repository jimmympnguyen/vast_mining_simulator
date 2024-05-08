import unittest
import mock

from mining_simulator.coordinator import MiningCoordinator
from mining_simulator.mining_site import MiningSite
from mining_simulator.mining_station import UnloadStation
from mining_simulator.mining_truck import MiningTruck


class TestMiningStation(unittest.TestCase):
    def setUp(self):
        self.coordinator = MiningCoordinator(num_trucks=1, num_stations=2)

    def test_instances(self):
        self.assertTrue(len(self.coordinator.mining_sites) == 1)
        self.assertTrue(len(self.coordinator.trucks) == 1)
        self.assertTrue(len(self.coordinator.deposit_stations) == 2)

        self.assertTrue(isinstance(self.coordinator.mining_sites[0], MiningSite))
        self.assertTrue(isinstance(self.coordinator.trucks[0], MiningTruck))
        self.assertTrue(isinstance(self.coordinator.deposit_stations[0], UnloadStation))

    @mock.patch.object(MiningSite, "add_truck_to_queue")
    def test_add_truck_to_mine(self, mock_site: mock.Mock):
        truck = self.coordinator.trucks[0]
        truck.timer = 5
        truck.current_action = truck.Actions.TRAVEL_TO_MINE

        self.coordinator.time_step()
        mock_site.assert_not_called()

        truck.timer = 0
        self.coordinator.time_step()
        mock_site.assert_called()

    @mock.patch.object(UnloadStation, "add_truck_to_queue")
    def test_add_truck_to_unloading_site(self, mock_site: mock.Mock):
        truck = self.coordinator.trucks[0]
        truck.timer = 5
        truck.current_action = truck.Actions.TRAVEL_TO_UNLOAD

        self.coordinator.time_step()
        mock_site.assert_not_called()

        truck.timer = 0
        self.coordinator.time_step()
        mock_site.assert_called()

    @mock.patch.object(MiningTruck, "take_action")
    @mock.patch.object(MiningSite, "manage_queue")
    @mock.patch.object(UnloadStation, "manage_queue")
    def test_time_step(
        self,
        mock_unload_queue: mock.Mock,
        mock_mine_queue: mock.Mock,
        mock_action: mock.Mock,
    ):
        self.coordinator.time_step()
        self.assertTrue(mock_unload_queue.call_count == 2)
        self.assertTrue(mock_mine_queue.call_count == 1)
        self.assertTrue(mock_action.call_count == 1)
