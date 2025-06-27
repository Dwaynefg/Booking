from abc import ABC, abstractmethod

class Vehicle(ABC):
    COST_MODIFIERS = {
        "Car4Seater": 1.0,
        "Car6Seater": 1.1,
        "Minivan": 1.1,
        "Van": 1.2,
        "Bike": 0.8,
        "Motorcycle": 0.9,
    }

    def __init__(self, name, category, cost_per_mile, capacity):
        self.name = name
        self.category = category      # e.g., "Car"
        self.cost_per_mile = cost_per_mile
        self.capacity = capacity

    def calculate_cost(self, distance):
        # Use class name to get modifier
        modifier = self.COST_MODIFIERS.get(self.__class__.__name__, 1.0)
        return distance * self.cost_per_mile * modifier

class Car(Vehicle):
    def __init__(self, name, cost_per_mile, capacity):
        super().__init__(name, category="Car", cost_per_mile=cost_per_mile, capacity=capacity)

class Car4Seater(Car):
    def __init__(self, name, cost_per_mile):
        super().__init__(name, cost_per_mile, capacity=4)

class Car6Seater(Car):
    def __init__(self, name, cost_per_mile):
        super().__init__(name, cost_per_mile, capacity=6)

class Van(Vehicle):
    def __init__(self, name, cost_per_mile, capacity=12):
        super().__init__(name, category="Van", cost_per_mile=cost_per_mile, capacity=capacity)

class Minivan(Van):
    def __init__(self, name, cost_per_mile):
        super().__init__(name, cost_per_mile, capacity=7)

class Bike(Vehicle):
    def __init__(self, name, cost_per_mile, capacity=1):
        super().__init__(name, category="Bike", cost_per_mile=cost_per_mile, capacity=capacity)

class Motorcycle(Vehicle):
    def __init__(self, name, cost_per_mile, capacity=1):
        super().__init__(name, category="Motorcycle", cost_per_mile=cost_per_mile, capacity=capacity)
