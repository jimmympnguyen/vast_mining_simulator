import configparser

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
            if truck.current_action == truck.Actions.REQUEST_QUEUE:
                station = min(self.deposit_stations)
                print(f"adding truck {truck.id} to station {station.id}")
                station.add_truck_to_queue(truck)
            elif truck.current_action == truck.Actions.REQUEST_MINE:
                mine = min(self.mining_sites)
                mine.add_truck_to_queue(truck)

            truck.take_action()
            print(truck)

    def log_statistics(self) -> None:
        for truck in self.trucks:
            truck.output_statistics()
        pass


class MinigTruckSimulator:
    """
    Class to configure and execute the mining simulation. Will run until enough
    time steps have elapsed the maximum defined time steps.
    """

    def __init__(self) -> None:
        self.parameters = configparser.ConfigParser()
        self.parameters.read("./sim_parameters.ini")

        self.time_step = 0
        self.timestep_size_minutes = self.parameters.getint("sim", "sim_step_minutes")
        self.max_timestep_minutes = (
            self.parameters.getint("sim", "sim_duration_hours") * 60.0
        )

        num_trucks = self.parameters.getint("sim", "num_trucks")
        num_stations = self.parameters.getint("sim", "num_stations")
        self.coordinator = MiningCoordinator(num_trucks, num_stations)

    def run_simulation(self) -> None:
        """Run simulation enough time steps have elapsed the maximum defined time steps."""

        while self.time_step < self.max_timestep_minutes:
            print(f"Current time step: {self.time_step}")
            self.coordinator.time_step()
            self.time_step += self.timestep_size_minutes


if __name__ == "__main__":
    sim = MinigTruckSimulator()
    sim.run_simulation()
