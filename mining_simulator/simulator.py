from mining_simulator.mining_site import MiningSite
from mining_simulator.mining_station import UnloadStation
from mining_simulator.mining_truck import MiningTruck


class MiningCoordinator:
    def __init__(self, num_trucks: int, num_stations: int):
        self.num_trucks = num_trucks
        self.num_stations = num_stations
        self.deposit_stations = [UnloadStation() for _ in range(self.num_stations)]
        self.trucks = [MiningTruck() for _ in range(self.num_trucks)]
        self.mining_sites = [MiningSite() for _ in range(self.num_trucks)]

    def time_step(self):
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


class MinigTruckSimulator:
    def __init__(self, num_trucks: int, num_stations: int):
        self.coordinator = MiningCoordinator(num_trucks, num_stations)
        self.time_step = 0
        self.max_timestep = 50

    def run_simulation(self):
        while self.time_step < self.max_timestep:
            print(f"Current time step: {self.time_step}")
            self.coordinator.time_step()
            self.time_step += 5
        for truck in self.coordinator.trucks:
            truck.output_statistics()


if __name__ == "__main__":
    sim = MinigTruckSimulator(
        num_trucks=1,
        num_stations=1,
    )
    sim.run_simulation()
