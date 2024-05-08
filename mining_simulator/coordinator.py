from mining_simulator.mining_site import MiningSite
from mining_simulator.mining_station import UnloadStation
from mining_simulator.mining_truck import MiningTruck


class MiningCoordinator:
    """
    Top-level coordinator to manage all instances of mining trucks, unloading stations, and mines.
    Has each mine and unloading station manager their queues and add trucks to queues when in the
    appropriate state. Finally moves the state forwards by one time step.

    Args:
        num_trucks: number of MiningTruck instances to create.
        num_stations: number of UnloadingStation instances to create.
    """

    def __init__(self, num_trucks: int, num_stations: int) -> None:
        self.deposit_stations = [UnloadStation() for _ in range(num_stations)]
        self.trucks = [MiningTruck() for _ in range(num_trucks)]
        self.mining_sites = [MiningSite() for _ in range(num_trucks)]

    def time_step(self) -> None:
        """
        Moves the simulation forwards by one time step by having each instance execute the housekeeping
        that it is responsible for. Coordinates allocation of trucks to mines or unloading stations depending
        on state.
        """

        for mine in self.mining_sites:
            mine.manage_queue()
        for station in self.deposit_stations:
            station.manage_queue()

        for truck in self.trucks:
            if (
                truck.current_action == truck.Actions.TRAVEL_TO_UNLOAD
                and truck.timer == 0
            ):
                station = min(self.deposit_stations)
                print(f"adding truck {truck.id} to station {station.id}")
                station.add_truck_to_queue(truck)
            elif (
                truck.current_action == truck.Actions.TRAVEL_TO_MINE
                and truck.timer == 0
            ):
                mine = min(self.mining_sites)
                print(f"adding truck {truck.id} to mine {mine.id}")
                mine.add_truck_to_queue(truck)
        for truck in self.trucks:
            truck.take_action()
            print(truck)

    def log_statistics(self) -> None:
        for truck in self.trucks:
            truck.output_statistics()
        pass