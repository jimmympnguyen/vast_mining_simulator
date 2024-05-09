import configparser
import itertools
import logging
from enum import Enum

logger: logging.Logger = logging.getLogger(__name__)


class MiningTruck:
    """
    Class to represent a mining truck. Used to manage its state machine
    and activity timers. Records its statistics to measure performance.
    """

    class Actions(Enum):
        """Enumerations for possible truck actions to control state machine."""

        WAITING = "Waiting"
        TRAVEL_TO_MINE = "Travel to Mine"
        TRAVEL_TO_UNLOAD = "Travel to Unload"
        UNLOADING = "Unloading"
        MINING = "Mining"

    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.timer = 0
        self.current_action = self.Actions.TRAVEL_TO_MINE

        self.parameters = configparser.ConfigParser()
        self.parameters.read("./mining_simulator/sim_parameters.ini")
        self.travel_time_minutes = self.parameters.getint(
            "truck", "travel_time_minutes"
        )
        self.sim_step_time_minutes = self.parameters.getint("sim", "sim_step_minutes")

        self.time_waiting = 0
        self.time_mining = 0
        self.time_travelling = 0
        self.time_unloading = 0
        self.units_mined = 0
        self.idk = 0

    def __str__(self) -> str:
        return f"Truck {self.id} is currently {self.current_action.value} with {self.timer} minutes left.\n"

    def __add__(self, other) -> int:
        """Addition dunder override to help sum total wait times at unloading queues."""

        return self.timer + other

    def __radd__(self, other) -> int:
        """Addition dunder override to help sum total wait times at unloading queues."""

        if other == 0:
            return self.timer
        else:
            return self.__add__(other)

    def take_action(self):
        """
        Progress the state timer forward by one step. If action is complete, move to the next state.
        Tally time spent in each state to capture performance metrics.
        """
        self.increment_counters()
        if self.timer == 0:
            self.current_action = self.next_action()
            if (
                self.current_action == self.Actions.TRAVEL_TO_MINE
                or self.current_action == self.Actions.TRAVEL_TO_UNLOAD
            ):
                self.timer = self.travel_time_minutes
        else:
            self.timer -= self.sim_step_time_minutes

    def next_action(self) -> Actions:
        """
        State machine control, see README for more details.

        Returns:
            Returns next truck state Action.
        """

        if self.current_action == self.Actions.MINING:
            return self.Actions.TRAVEL_TO_UNLOAD
        elif self.current_action == self.Actions.UNLOADING:
            return self.Actions.TRAVEL_TO_MINE
        elif self.current_action == self.Actions.TRAVEL_TO_MINE:
            return self.Actions.MINING
        elif self.current_action == self.Actions.TRAVEL_TO_UNLOAD:
            return self.Actions.UNLOADING
        else:
            # default state
            return self.current_action

    def increment_counters(self):
        """Helper function to increment counters based on current action."""

        if self.current_action == self.Actions.WAITING:
            self.time_waiting += self.sim_step_time_minutes
        elif (
            self.current_action == self.Actions.TRAVEL_TO_MINE
            or self.current_action == self.Actions.TRAVEL_TO_UNLOAD
        ):
            self.time_travelling += self.sim_step_time_minutes
        elif self.current_action == self.Actions.MINING:
            self.time_mining += self.sim_step_time_minutes
        elif self.current_action == self.Actions.UNLOADING:
            self.time_unloading += self.sim_step_time_minutes
        else:
            self.idk += self.sim_step_time_minutes

    def output_statistics(self):
        """Function to log performance of mining truck."""

        logger.info(
            f"Truck {self.id} mined a total of {self.units_mined} units He-3.\n"
            f"Truck {self.id} total time spent: \n"
            f"  {self.time_mining} minutes mining.\n"
            f"  {self.time_travelling} minutes travelling.\n"
            f"  {self.time_unloading} minutes unloading.\n"
            f"  {self.time_waiting} minutes waiting.\n"
            f"  {self.idk} minutes idling.\n"
        )
