import configparser
import itertools

from mining_simulator.mining_truck import MiningTruck


class UnloadStation:
    """
    Class to represent an unloading station. Used to manage the addition and removal
    of mining trucks from its queue. Records its statistics to measure performance.
    """

    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.queue: list[MiningTruck] = []

        self.parameters = configparser.ConfigParser()
        self.parameters.read("./sim_parameters.ini")
        self.unload_time_minutes = self.parameters.getint(
            "unloading", "unload_time_minutes"
        )
        self.sim_step_time_minutes = self.parameters.getint("sim", "sim_step_minutes")

        self.current_wait_time = 0
        self.total_wait_time = 0
        self.units_deposited = 0

    def __lt__(self, other) -> bool:
        """Comparison dunder override on wait time to use min to sort."""
        return self.current_wait_time < other.current_wait_time

    def __eq__(self, other) -> bool:
        """Comparison dunder override on wait time to use min to sort."""
        return self.current_wait_time == other.current_wait_time

    def __str__(self) -> str:
        return (
            f"Unload Station {self.id} has {len(self.queue)} waiting "
            f"Mining Trucks and a wait time of {self.current_wait_time} minutes."
        )

    def add_truck_to_queue(self, truck: MiningTruck) -> None:
        """Add a mining truck to the unloading queue. If there are no other trucks present
        then the truck can immediately begin unloading. Otherwise the truck will be set to
        waiting in the queue. Updates the unloading stations current wait time.

        Sets the truck object's timer and action either waiting or unloading.

        Args:
            truck: an instance of a MiningTruck.
        """

        if self.queue:
            truck.current_action = truck.Actions.WAITING
        else:
            truck.current_action = truck.Actions.UNLOADING
        self.queue.append(truck)
        truck.timer = self.unload_time_minutes
        self.current_wait_time = sum(self.queue)

    def manage_queue(self) -> None:
        """
        Checks the status of the queue, if there is a truck present check its timer,
        if the timer is 0 then the truck is done unloading and will be removed from the queue.
        Once a truck is finished unloading, increment the total number of deposits by the truck and unloading site.
        If there is a truck at the front of the queue and waiting, change its action to unloading.
        Tally the total cumulated wait time for this queue.
        """
        if self.queue:
            # increment the queue's total accumulated wait time by the length of the queue * the time step size
            # but not couting the truck at the front of the queue, since it's not waiting.
            self.total_wait_time += len(self.queue[1:]) * self.sim_step_time_minutes

            truck = self.queue[0]
            if truck.timer == 0:
                # truck at front of queue finished unloading, remove it
                print(
                    f"Truck {truck.id} has completed is unloading at station {self.id}!"
                )
                truck.units_mined += 1
                self.units_deposited += 1
                self.queue.pop(0)

            if self.queue:
                truck = self.queue[0]
                if truck.current_action == truck.Actions.WAITING:
                    # if there is a truck waiting in front of the line, let it begin unloading
                    truck.current_action = truck.Actions.UNLOADING
                    print(
                        f"Truck {truck.id} has moved to front of queue at station {self.id}!"
                    )
