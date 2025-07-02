from abc import ABC

class Vehicle(ABC):
    TAX_RATES = {
        "Car4Seater": 0.03,
        "Car6Seater": 0.03,
        "Minivan": 0.03,
        "Van": 0.03,
        "Motorcycle": 0.03,
    }

    BASE_FARES = {
        "Car4Seater": 100,
        "Car6Seater": 120,
        "Minivan": 200,
        "Van": 250,
        "Motorcycle": 50,
    }

    COST_PER_KM = {
        "Car4Seater": 15,
        "Car6Seater": 17,
        "Minivan": 18,
        "Van": 20,
        "Motorcycle": 10,
    }

    AVERAGE_SPEED = {
        "Car4Seater": 60,
        "Car6Seater": 60,
        "Minivan": 50,
        "Van": 50,
        "Motorcycle": 70,
    }

    def __init__(self, vehicle_name, vehicle_type, capacity):
        self.vehicle_name = vehicle_name
        self.vehicle_type = vehicle_type
        self.capacity = capacity

    @property
    def cost_per_km(self):
        # Dynamically get cost_per_km from class dict, so it can be changed globally
        return self.COST_PER_KM.get(self.vehicle_type, 0)

    @property
    def average_speed(self):
        # Dynamically get average_speed from class dict, so it can be changed globally
        return self.AVERAGE_SPEED.get(self.vehicle_type, 60)  # Default to 60 km/h

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

    def calculate_eta_minutes(self, distance_km):
        """
        Calculate estimated time of arrival in minutes
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            ETA in minutes (float)
        """
        if distance_km <= 0:
            return 0
        
        # Time = Distance / Speed (in hours), then convert to minutes
        time_hours = distance_km / self.average_speed
        time_minutes = time_hours * 60
        return time_minutes

    def get_eta_formatted(self, distance_km):
        """
        Get formatted ETA string
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            Formatted ETA string (e.g., "25 minutes", "1 hour 15 minutes")
        """
        total_minutes = self.calculate_eta_minutes(distance_km)
        
        if total_minutes < 1:
            return "Less than 1 minute"
        elif total_minutes < 60:
            return f"{int(total_minutes)} minute{'s' if int(total_minutes) != 1 else ''}"
        else:
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            
            if minutes == 0:
                return f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"

    def to_dict(self):
        return {
            "vehicleType": self.vehicle_type,
            "vehicleName": self.vehicle_name,
            "cost_per_km": self.cost_per_km,
            "average_speed": self.average_speed,
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