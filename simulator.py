import configparser
import logging
import sys

from mining_simulator.coordinator import MiningCoordinator

logger: logging.Logger = logging.getLogger(__name__)


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

        self.num_trucks = self.parameters.getint("sim", "num_trucks")
        self.num_stations = self.parameters.getint("sim", "num_stations")
        self.coordinator = MiningCoordinator(self.num_trucks, self.num_stations)

    def run_simulation(self) -> None:
        """Run simulation enough time steps have elapsed the maximum defined time steps."""

        while self.time_step < self.max_timestep_minutes:
            logger.debug(f"Current time step: {self.time_step}")
            self.coordinator.time_step()
            self.time_step += self.timestep_size_minutes

    def setup_logger(self) -> None:
        """Setup logging."""
        verbose = False
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        if verbose:
            handler.setLevel(logging.DEBUG)
        else:
            handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        file_handler = logging.FileHandler("test.log")
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    def main(self) -> None:
        """Simulation entry point."""
        self.setup_logger()
        logger.info(
            f"Beginning simulation with {self.num_trucks} mining trucks and {self.num_stations} deposit stations.\n"
        )
        self.run_simulation()
        logger.info("\nSimulation complete! Simulation results:\n")
        self.coordinator.output_truck_statistics()
        self.coordinator.output_unloading_site_statistics()


if __name__ == "__main__":
    sim = MinigTruckSimulator()
    sim.main()
