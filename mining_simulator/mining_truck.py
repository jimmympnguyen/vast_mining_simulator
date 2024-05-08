import configparser
import itertools
from enum import Enum
from typing import Tuple


class MiningTruck:
    """
    Class to represent a mining truck. Used to manage its state machine
    and activity timers. Records its statistics to measure performance.
    """

    class Actions(Enum):
        """Enumerations for possible truck actions to control state machine."""

        WAITING = "Waiting"
        TRAVELLING = "Travelling"
        UNLOADING = "Unloading"
        MINING = "Mining"
        REQUEST_QUEUE = "Request Queue"
        REQUEST_MINE = "Request Mine"

    class Locations(Enum):
        """Enumerations for possible truck locations to control state machine."""

        MINE = "Mine"
        UNLOADING_STATION = "Unloading Station"

    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.timer = 0
        self.current_action = self.Actions.REQUEST_MINE
        self.current_location = self.Locations.MINE

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

        if self.timer == 0:
            self.current_action, self.current_location = self.next_action()
            if self.current_action == self.Actions.TRAVELLING:
                self.timer = self.travel_time_minutes
        else:
            self.timer -= self.sim_step_time_minutes
        self.increment_counters()

    def next_action(self) -> Tuple[Actions, Locations]:
        """
        State machine control, see README for more details.

        Returns:
            tuple of next state actions and locations.
        """

        # finished mining or unloading, start travelling to next location
        if self.current_action == self.Actions.MINING:
            return (self.Actions.TRAVELLING, self.Locations.UNLOADING_STATION)
        elif self.current_action == self.Actions.UNLOADING:
            return (self.Actions.TRAVELLING, self.Locations.MINE)
        elif self.current_action == self.Actions.TRAVELLING:
            # finished travelling
            if self.current_location == self.Locations.MINE:
                return (self.Actions.REQUEST_MINE, self.current_location)
            elif self.current_location == self.Locations.UNLOADING_STATION:
                return (self.Actions.REQUEST_QUEUE, self.current_location)
        else:
            # default state
            return (self.current_action, self.current_location)

    def increment_counters(self):
        """Helper function to increment counters based on current action."""

        if self.current_action == self.Actions.WAITING:
            self.time_waiting += self.sim_step_time_minutes
        elif self.current_action == self.Actions.TRAVELLING:
            self.time_travelling += self.sim_step_time_minutes
        elif self.current_action == self.Actions.MINING:
            self.time_mining += self.sim_step_time_minutes
        elif self.current_action == self.Actions.UNLOADING:
            self.time_unloading += self.sim_step_time_minutes
        else:
            self.idk += self.sim_step_time_minutes

    def output_statistics(self):
        """Helper function to format performance of mining truck."""

        print(
            f"Truck {self.id} mined a total of {self.units_mined}. "
            f"Spent {self.time_mining} minutes mining. "
            f"Spent {self.time_travelling} minutes travelling. "
            f"Spent {self.time_unloading} minutes unloading. "
            f"Spent {self.time_waiting} minutes waiting. "
            f"Spent {self.idk} minutes messing around. "
        )
