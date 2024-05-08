import unittest

from mining_simulator.mining_site import MiningSite
from mining_simulator.mining_truck import MiningTruck


class TestMiningStation(unittest.TestCase):
    def setUp(self):
        self.mining_site1 = MiningSite()
        self.mining_site2 = MiningSite()
        self.mining_truck = MiningTruck()

    def test_queue_length_empty(self):
        available_mine = min(self.mining_site1, self.mining_site2)
        self.assertTrue(available_mine.id == self.mining_site1.id)

    def test_queue_length_site1(self):
        self.mining_site1.queue.append(self.mining_truck)
        available_mine = min(self.mining_site1, self.mining_site2)
        self.assertTrue(available_mine.id == self.mining_site2.id)

    def test_queue_length_site2(self):
        self.mining_site2.queue.append(self.mining_truck)
        available_mine = min(self.mining_site1, self.mining_site2)
        self.assertTrue(available_mine.id == self.mining_site1.id)

    def test_add_truck_to_empty_queue(self):
        result = self.mining_site1.add_truck_to_queue(self.mining_truck)
        self.assertTrue(result)
        self.assertTrue(self.mining_truck.timer > 0)
        self.assertTrue(self.mining_truck.current_action == self.mining_truck.Actions.MINING)
        self.assertTrue(len(self.mining_site1.queue) == 1)

    def test_add_truck_to_full_queue(self):
        result = self.mining_site1.add_truck_to_queue(self.mining_truck)
        self.assertTrue(result)
        self.assertTrue(len(self.mining_site1.queue) == 1)

        result = self.mining_site1.add_truck_to_queue(self.mining_truck)
        self.assertFalse(result)
        self.assertTrue(len(self.mining_site1.queue) == 1)

    def test_manage_queue(self):
        self.mining_site1.add_truck_to_queue(self.mining_truck)
        self.assertTrue(self.mining_truck.timer > 0)
        self.assertTrue(len(self.mining_site1.queue) == 1)

        self.mining_site1.manage_queue()
        self.assertTrue(self.mining_truck.timer > 0)
        self.assertTrue(len(self.mining_site1.queue) == 1)

        self.mining_truck.timer = 0
        self.mining_site1.manage_queue()
        self.assertTrue(self.mining_truck.timer == 0)
        self.assertTrue(len(self.mining_site1.queue) == 0)




