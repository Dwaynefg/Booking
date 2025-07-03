from .distance_calculator import DistanceCalculator
from .vehicle import Vehicle, Car4Seater, Car6Seater, Minivan, Van, Motorcycle

class FareCalculator:
    """Handles fare calculation based on distance and vehicle type"""
    
    # Map UI vehicle names to vehicle classes
    VEHICLE_TYPE_MAPPING = {
        "Car(4 Seater)": "Car4Seater",
        "Car(6 Seater)": "Car6Seater", 
        "Mini Van": "Minivan",
        "Van": "Van",
        "Motorcycle": "Motorcycle"
    }
    
    def __init__(self):
        self.distance_calculator = DistanceCalculator()
        
    def calculate_fare(self, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, vehicle_type_name):
        """
        Calculate total fare including base fare, distance cost, and tax
        
        Args:
            pickup_lat, pickup_lng: Pickup location coordinates
            dropoff_lat, dropoff_lng: Dropoff location coordinates  
            vehicle_type_name: Vehicle type name from UI (e.g., "Car(4 Seater)")
            
        Returns:
            Dictionary containing fare breakdown and total
        """
        try:
            # Calculate distance in kilometers
            distance_km = self.distance_calculator.calculate_distance_km(
                pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
            )
            
            # Get vehicle type for calculations
            vehicle_class_name = self.VEHICLE_TYPE_MAPPING.get(vehicle_type_name)
            if not vehicle_class_name:
                raise ValueError(f"Unknown vehicle type: {vehicle_type_name}")
            
            # Get pricing information from Vehicle class
            base_fare = Vehicle.BASE_FARES.get(vehicle_class_name, 0)
            cost_per_km = Vehicle.COST_PER_KM.get(vehicle_class_name, 0)
            tax_rate = Vehicle.TAX_RATES.get(vehicle_class_name, 0.03)
            
            # Calculate costs
            distance_cost = distance_km * cost_per_km
            subtotal = base_fare + distance_cost
            tax_amount = subtotal * tax_rate
            total_fare = subtotal + tax_amount
            
            return {
                'distance_km': round(distance_km, 2),
                'distance_miles': round(distance_km * DistanceCalculator.KM_TO_MILES, 2),
                'base_fare': base_fare,
                'cost_per_km': cost_per_km,
                'distance_cost': round(distance_cost, 2),
                'subtotal': round(subtotal, 2),
                'tax_rate': tax_rate,
                'tax_amount': round(tax_amount, 2),
                'total_fare': round(total_fare, 2),
                'vehicle_type': vehicle_type_name,
                'formatted_distance': self.distance_calculator.format_distance(
                    pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
                )
            }
            
        except Exception as e:
            print(f"Error calculating fare: {e}")
            return {
                'distance_km': 0,
                'distance_miles': 0,
                'base_fare': 0,
                'cost_per_km': 0,
                'distance_cost': 0,
                'subtotal': 0,
                'tax_rate': 0,
                'tax_amount': 0,
                'total_fare': 0,
                'vehicle_type': vehicle_type_name,
                'formatted_distance': "0.00 km (0.00 miles)",
                'error': str(e)
            }
    
    def get_fare_for_all_vehicles(self, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng):
        """
        Calculate fares for all available vehicle types
        
        Args:
            pickup_lat, pickup_lng: Pickup location coordinates
            dropoff_lat, dropoff_lng: Dropoff location coordinates
            
        Returns:
            Dictionary with vehicle types as keys and fare info as values
        """
        fares = {}
        
        for ui_vehicle_name in self.VEHICLE_TYPE_MAPPING.keys():
            fare_info = self.calculate_fare(
                pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, ui_vehicle_name
            )
            fares[ui_vehicle_name] = fare_info
            
        return fares
    
    def format_fare_display(self, fare_info):
        """
        Format fare information for display in UI
        
        Args:
            fare_info: Dictionary from calculate_fare method
            
        Returns:
            Formatted string for display
        """
        if fare_info.get('error'):
            return "₱ 0.00"
        
        total_fare = fare_info.get('total_fare', 0)
        return f"₱ {total_fare:.2f}"
    
    def get_fare_breakdown_text(self, fare_info):
        """
        Get detailed fare breakdown as formatted text
        
        Args:
            fare_info: Dictionary from calculate_fare method
            
        Returns:
            Multi-line string with fare breakdown
        """
        if fare_info.get('error'):
            return f"Error calculating fare: {fare_info['error']}"
        
        breakdown = f"""Distance: {fare_info['formatted_distance']}
Base Fare: ₱ {fare_info['base_fare']:.2f}
Distance Cost: ₱ {fare_info['distance_cost']:.2f} ({fare_info['distance_km']:.2f} km × ₱ {fare_info['cost_per_km']:.2f}/km)
Subtotal: ₱ {fare_info['subtotal']:.2f}
Tax ({fare_info['tax_rate']*100:.1f}%): ₱ {fare_info['tax_amount']:.2f}
Total Fare: ₱ {fare_info['total_fare']:.2f}"""
        
        return breakdown
    
    @staticmethod
    def update_vehicle_prices():
        """
        Static method to update vehicle pricing if needed
        This allows dynamic price updates without recreating the calculator
        """
        # This method can be used to update Vehicle class pricing
        # Example: Vehicle.BASE_FARES["Car4Seater"] = 120
        pass
    
    def get_distance_info(self, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng):
        """
        Get just the distance information without fare calculation
        
        Args:
            pickup_lat, pickup_lng: Pickup location coordinates
            dropoff_lat, dropoff_lng: Dropoff location coordinates
            
        Returns:
            Dictionary with distance information
        """
        try:
            distance_km = self.distance_calculator.calculate_distance_km(
                pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
            )
            
            return {
                'distance_km': round(distance_km, 2),
                'distance_miles': round(distance_km * DistanceCalculator.KM_TO_MILES, 2),
                'formatted_distance': self.distance_calculator.format_distance(
                    pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
                ),
                'center_point': self.distance_calculator.get_center_point(
                    pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
                ),
                'zoom_level': self.distance_calculator.get_zoom_level_for_distance(
                    pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
                )
            }
        except Exception as e:
            print(f"Error getting distance info: {e}")
            return {
                'distance_km': 0,
                'distance_miles': 0,
                'formatted_distance': "0.00 km (0.00 miles)",
                'center_point': (pickup_lat, pickup_lng),
                'zoom_level': 15,
                'error': str(e)
            }