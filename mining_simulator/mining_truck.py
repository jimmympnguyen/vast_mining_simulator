import itertools
from enum import Enum
from typing import Tuple

class MiningTruck:
    class Actions(Enum):
        WAITING = "Waiting"
        TRAVELLING = "Travelling"
        UNLOADING = "Unloading"
        MINING = "Mining"
        REQUEST_QUEUE = "Request Queue"
        REQUEST_MINE = "Request Mine"

    class Locations(Enum):
        MINE = "Mine"
        UNLOADING_STATION = "Unloading Station"

    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.timer = 0
        self.current_action = self.Actions.REQUEST_MINE
        self.current_location = self.Locations.MINE

        self.time_waiting = 0
        self.time_mining = 0
        self.time_travelling = 0
        self.time_unloading = 0
        self.units_mined = 0

    def __str__(self) -> str:
        return (
            f"Truck {self.id} is currently {self.current_action.value} with {self.timer} minutes left.\n"
        )

    def __add__(self, other) -> int:
        return self.timer + other

    def __radd__(self, other) -> int:
        if other == 0:
            return self.timer
        else:
            return self.__add__(other)

    def take_action(self):
        if self.timer == 0:
            self.current_action, self.current_location = self.next_action()
            if self.current_action == self.Actions.TRAVELLING:
                self.timer = 30
        else:
            self.timer -= 5
        self.increment_counters()

    def next_action(self) -> Tuple[Actions, Locations]:
        # finished mining or unloading, start travelling to next location
        if self.current_action == self.Actions.MINING:
            return(self.Actions.TRAVELLING, self.Locations.UNLOADING_STATION)
        elif self.current_action == self.Actions.UNLOADING:
            return(self.Actions.TRAVELLING, self.Locations.MINE)
        elif self.current_action == self.Actions.TRAVELLING:
            # finished travelling and arrived to location, waiting for assignment
            if self.current_location == self.Locations.MINE:
                return(self.Actions.REQUEST_MINE, self.current_location)
            elif self.current_location == self.Locations.UNLOADING_STATION:
                return(self.Actions.REQUEST_QUEUE, self.current_location)
        else:
            # default wait state
            return(self.current_action, self.current_location)

    def increment_counters(self):
        # truck needs to know the time step, dont love having 5 as magic number
        TIME_STEP = 5
        if self.current_action == self.Actions.WAITING:
            self.time_waiting += TIME_STEP
        if self.current_action == self.Actions.TRAVELLING:
            self.time_travelling += TIME_STEP
        if self.current_action == self.Actions.MINING:
            self.time_mining += TIME_STEP
        if self.current_action == self.Actions.UNLOADING:
            self.time_unloading += TIME_STEP

    def output_statistics(self):
        print(
            f"Truck {self.id} mined a total of {self.units_mined}. "
            f"Spent {self.time_mining} minutes mining. "
            f"Spent {self.time_travelling} minutes travelling. "
            f"Spent {self.time_unloading} minutes unloading. "
            f"Spent {self.time_waiting} minutes waiting. "
        )
