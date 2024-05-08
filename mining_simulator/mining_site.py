import itertools
import random

from mining_simulator.mining_truck import MiningTruck


class MiningSite:
    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.queue: list[MiningTruck] = []

    def __lt__(self, other) -> bool:
        return len(self.queue) < len(other.queue)

    def __eq__(self, other) -> bool:
        return len(self.queue) == len(other.queue)

    def add_truck_to_queue(self, truck: MiningTruck) -> bool:
        if self.queue:
            # this will never happen, but just in case
            return False

        self.queue.append(truck)
        truck.timer = random.randint(1, 5) * 5
        truck.current_action = truck.Actions.MINING
        print(f"Truck {truck.id} is now mining at mine {self.id} with duration of {truck.timer}!")
        return True

    def manage_queue(self) -> None:
        if self.queue:
            truck = self.queue[0]
            if truck.timer == 0:
                print(f"Truck {truck.id} has completed mining at mine {self.id}!")
                self.queue.pop(0)