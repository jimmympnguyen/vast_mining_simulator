import itertools

from mining_simulator.mining_truck import MiningTruck


class UnloadStation:
    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.queue: list[MiningTruck] = []
        self.current_wait_time = 0
        self.total_wait_time = 0
        self.units_deposited = 0

    def __lt__(self, other) -> bool:
        return self.current_wait_time < other.current_wait_time

    def __eq__(self, other) -> bool:
        return self.current_wait_time == other.current_wait_time

    def __str__(self) -> str:
        return (
            f"Unload Station {self.id} has {len(self.queue)} waiting "
            f"Mining Trucks and a wait time of {self.current_wait_time} minutes."
        )

    def add_truck_to_queue(self, truck: MiningTruck) -> None:
        if self.queue:
            truck.current_action = truck.Actions.WAITING
        else:
            truck.current_action = truck.Actions.UNLOADING
        self.queue.append(truck)
        truck.timer = 5  # set to wait time
        self.current_wait_time = sum(self.queue)

    def manage_queue(self) -> None:
        if self.queue:
            truck = self.queue[0]
            self.total_wait_time += len(self.queue[1:]) * 5
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
