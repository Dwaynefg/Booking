from abc import ABC

class Vehicle(ABC):
    TAX_RATES = {
        "Car4Seater": 0.05,
        "Car6Seater": 0.05,
        "Minivan": 0.05,
        "Van": 0.06,
        "Motorcycle": 0.04,
    }

    BASE_FARES = {
        "Car4Seater": 100,
        "Car6Seater": 120,
        "Minivan": 150,
        "Van": 180,
        "Motorcycle": 50,
    }

    COST_PER_KM = {
        "Car4Seater": 15,
        "Car6Seater": 17,
        "Minivan": 18,
        "Van": 20,
        "Motorcycle": 10,
    }

    def __init__(self, vehicle_name, vehicle_type, capacity):
        self.vehicle_name = vehicle_name
        self.vehicle_type = vehicle_type
        self.capacity = capacity

    @property
    def cost_per_km(self):
        # Dynamically get cost_per_km from class dict, so it can be changed globally
        return self.COST_PER_KM.get(self.vehicle_type, 0)

    def calculate_cost(self, distance):
        return distance * self.cost_per_km

    def calculate_tax(self, distance):
        base_cost = self.calculate_cost(distance)
        tax_rate = self.TAX_RATES.get(self.vehicle_type, 0.0)
        return base_cost * tax_rate

    def calculate_cost_with_tax(self, distance):
        base_cost = self.calculate_cost(distance)
        tax = self.calculate_tax(distance)
        base_fare = self.BASE_FARES.get(self.vehicle_type, 0.0)
        total_base = base_cost + base_fare
        return total_base, tax

    def to_dict(self):
        return {
            "vehicleType": self.vehicle_type,
            "vehicleName": self.vehicle_name,
            "cost_per_km": self.cost_per_km,
            "capacity": self.capacity,
        }


class Car(Vehicle):
    def __init__(self, vehicle_name, vehicle_type, capacity):
        super().__init__(vehicle_name, vehicle_type, capacity)


class Car4Seater(Car):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Car4Seater", 4)


class Car6Seater(Car):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Car6Seater", 6)


class Van(Vehicle):
    def __init__(self, vehicle_name, vehicle_type, capacity=12):
        super().__init__(vehicle_name, vehicle_type, capacity)


class Minivan(Van):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Minivan", 7)


class Motorcycle(Vehicle):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Motorcycle", 1)
