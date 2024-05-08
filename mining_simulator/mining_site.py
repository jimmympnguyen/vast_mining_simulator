import configparser
import itertools
import random

from mining_simulator.mining_truck import MiningTruck


class MiningSite:
    """
    Class to represent a mining site. Used to manage the addition and removal
    of mining trucks from its queue.
    """

    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.queue: list[MiningTruck] = []
        self.parameters = configparser.ConfigParser()
        self.parameters.read("./mining_simulator/sim_parameters.ini")
        self.min_mine_time_hours = self.parameters.getint(
            "mining", "min_mining_time_hours"
        )
        self.max_mine_time_hours = self.parameters.getint(
            "mining", "max_mining_time_hours"
        )

    def __lt__(self, other) -> bool:
        """Comparison dunder override on queue length to use min to sort."""
        return len(self.queue) < len(other.queue)

    def __eq__(self, other) -> bool:
        """Comparison dunder override on queue length to use min to sort."""
        return len(self.queue) == len(other.queue)

    def add_truck_to_queue(self, truck: MiningTruck) -> bool:
        """Add a mining truck to the mining queue. Queue is maximum size of one and will return
        False if a second truck is attempts to add to the queue.

        Sets the truck object's timer and action to mining.

        Args:
            truck: an instance of a MiningTruck.

        Returns:
            True if addition to queue was successful, False otherwise.
        """

        if self.queue:
            # this will never happen, but just in case
            return False

        self.queue.append(truck)
        truck.timer = (
            random.randint(self.min_mine_time_hours, self.max_mine_time_hours) * 5.0
        )
        truck.current_action = truck.Actions.MINING
        print(
            f"Truck {truck.id} is now mining at mine {self.id} with duration of {truck.timer}!"
        )
        return True

    def manage_queue(self) -> None:
        """
        Checks the status of the queue, if there is a truck present check its timer,
        if the timer is 0 then the truck is done mining and will be removed from the queue.
        """

        if self.queue:
            truck = self.queue[0]
            if truck.timer == 0:
                print(f"Truck {truck.id} has completed mining at mine {self.id}!")
                self.queue.pop(0)

    def output_statistics(self):
        """Helper function to format performance of unloading site."""

        print(
            f"Truck {self.id} mined a total of {self.units_mined}. "
            f"Spent {self.time_mining} minutes mining. "
            f"Spent {self.time_travelling} minutes travelling. "
            f"Spent {self.time_unloading} minutes unloading. "
            f"Spent {self.time_waiting} minutes waiting. "
            f"Spent {self.idk} minutes messing around. "
        )
