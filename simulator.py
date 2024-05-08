import configparser

from mining_simulator.coordinator import MiningCoordinator


class MinigTruckSimulator:
    """
    Class to configure and execute the mining simulation. Will run until enough
    time steps have elapsed the maximum defined time steps.
    """

    def __init__(self) -> None:
        self.parameters = configparser.ConfigParser()
        self.parameters.read("./mining_simulator/sim_parameters.ini")

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
        self.coordinator.log_statistics()


if __name__ == "__main__":
    sim = MinigTruckSimulator()
    sim.run_simulation()
