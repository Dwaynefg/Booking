from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, name, cost_per_mile, capacity):
        self.name = name
        self.cost_per_mile = cost_per_mile
        self.capacity = capacity

    @abstractmethod
    def calculate_cost(self, distance):
        pass

class Car(Vehicle, ABC):
    def __init__(self, name, cost_per_mile, capacity):
        super().__init__(name, cost_per_mile, capacity)

    @abstractmethod
    def calculate_cost(self, distance):
        pass

class Car4Seater(Car):
    def __init__(self, name, cost_per_mile):
        super().__init__(name, cost_per_mile, capacity=4)

    def calculate_cost(self, distance):
        return distance * self.cost_per_mile

class Car6Seater(Car):
    def __init__(self, name, cost_per_mile):
        super().__init__(name, cost_per_mile, capacity=6)

    def calculate_cost(self, distance):
        return distance * self.cost_per_mile * 1.1

class Van(Vehicle):
    def __init__(self, name, cost_per_mile, capacity=12):
        super().__init__(name, cost_per_mile, capacity)

    def calculate_cost(self, distance):
        return distance * self.cost_per_mile * 1.2

class Minivan(Van):
    def __init__(self, name, cost_per_mile):
        super().__init__(name, cost_per_mile, capacity=7)

    def calculate_cost(self, distance):
        return distance * self.cost_per_mile * 1.1

class Bike(Vehicle):
    def __init__(self, name, cost_per_mile, capacity=1):
        super().__init__(name, cost_per_mile, capacity)

    def calculate_cost(self, distance):
        return distance * self.cost_per_mile * 0.8

class Motorcycle(Vehicle):
    def __init__(self, name, cost_per_mile, capacity=1):
        super().__init__(name, cost_per_mile, capacity)

    def calculate_cost(self, distance):
        return distance * self.cost_per_mile * 0.9
