import logging

from mining_simulator.mining_site import MiningSite
from mining_simulator.mining_truck import MiningTruck
from mining_simulator.unloading_station import UnloadStation

logger: logging.Logger = logging.getLogger(__name__)


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
        self.unloading_stations = [UnloadStation() for _ in range(num_stations)]
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
        for station in self.unloading_stations:
            station.manage_queue()

        for truck in self.trucks:
            if (
                truck.current_action == truck.Actions.TRAVEL_TO_UNLOAD
                and truck.timer == 0
            ):
                station = min(self.unloading_stations)
                logger.debug(f"adding truck {truck.id} to station {station.id}")
                station.add_truck_to_queue(truck)
            elif (
                truck.current_action == truck.Actions.TRAVEL_TO_MINE
                and truck.timer == 0
            ):
                mine = min(self.mining_sites)
                logger.debug(f"adding truck {truck.id} to mine {mine.id}")
                mine.add_truck_to_queue(truck)
        for truck in self.trucks:
            truck.take_action()
            # print(truck)

    def output_truck_statistics(self) -> None:
        sorted_trucks = sorted(
            self.trucks, key=lambda truck: truck.units_mined, reverse=True
        )
        for truck in sorted_trucks:
            truck.output_statistics()

    def output_unloading_site_statistics(self) -> None:
        sorted_sites = sorted(
            self.unloading_stations, key=lambda site: site.units_deposited, reverse=True
        )
        for site in sorted_sites:
            site.output_statistics()
