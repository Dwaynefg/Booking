from abc import ABC, abstractmethod

class Vehicle(ABC):
    TAX_RATES = {
        "Car4Seater": 0.05,  # 5% Tax
        "Car6Seater": 0.05,  # 5% Tax
        "Minivan": 0.05,     # 5% Tax
        "Van": 0.06,         # 6% Tax (Larger vehicle, slightly higher tax)
        "Motorcycle": 0.04,  # 4% Tax (Smaller, more economical vehicle)
    }

    BASE_FARES = {
        "Car4Seater": 100,  # Base fare for smaller vehicles
        "Car6Seater": 120,  # Slightly higher base fare for 6-seater
        "Minivan": 150,     # Larger vehicle base fare
        "Van": 180,         # Higher base fare for vans
        "Motorcycle": 50,   # Lower base fare for motorcycles
    }

    COST_PER_KM = {
        "Car4Seater": 15,   # Cost per km for 4-seater cars
        "Car6Seater": 17,   # Slightly higher cost for 6-seater
        "Minivan": 18,      # Minivan's higher operational cost per km
        "Van": 20,          # Vans typically have higher operational costs
        "Motorcycle": 10,   # Motorcycles are more economical
    }

    def __init__(self, vehicle_name, vehicle_type, cost_per_km, capacity):
        self.vehicle_name = vehicle_name  # Specific name of the vehicle (e.g., Toyota Camry)
        self.vehicle_type = vehicle_type  # Type of the vehicle (e.g., Car4Seater)
        self.cost_per_km = cost_per_km
        self.capacity = capacity

    def calculate_cost(self, distance):
        """Calculate the cost for the given distance."""
        return distance * self.cost_per_km

    def calculate_tax(self, distance):
        """Calculate the tax based on the vehicle's tax rate."""
        base_cost = self.calculate_cost(distance)
        tax_rate = self.TAX_RATES.get(self.vehicle_type, 0.0)
        return base_cost * tax_rate

    def calculate_cost_with_tax(self, distance):
        """Calculate the total cost with tax included."""
        base_cost = self.calculate_cost(distance)
        tax = self.calculate_tax(distance)  # Use the new tax function
        base_fare = self.BASE_FARES.get(self.vehicle_type, 0.0)
        total_base = base_cost + base_fare
        return total_base, tax

    def to_dict(self):
        """Convert the vehicle object to a dictionary representation."""
        return {
            "vehicleType": self.vehicle_type,
            "vehicleName": self.vehicle_name,
            "cost_per_km": self.cost_per_km,
            "capacity": self.capacity,
        }


# Subclasses for different vehicle types
class Car(Vehicle):
    def __init__(self, vehicle_name, vehicle_type, cost_per_km, capacity):
        super().__init__(vehicle_name, vehicle_type, cost_per_km, capacity)

class Car4Seater(Car):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Car4Seater", 15, 4)

class Car6Seater(Car):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Car6Seater", 17, 6)

class Van(Vehicle):
    def __init__(self, vehicle_name, vehicle_type, cost_per_km, capacity=12):
        super().__init__(vehicle_name, vehicle_type, cost_per_km, capacity)

class Minivan(Van):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Minivan", 18, 7)

class Motorcycle(Vehicle):
    def __init__(self, vehicle_name):
        super().__init__(vehicle_name, "Motorcycle", 10, 1)

