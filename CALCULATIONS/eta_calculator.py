import math
from datetime import datetime, timedelta
from CALCULATIONS.distance_calculator import DistanceCalculator
from CALCULATIONS.vehicle import Vehicle, Car4Seater, Car6Seater, Minivan, Van, Motorcycle

class ETACalculator:
    """
    Utility class for calculating estimated time of arrival (ETA) between geographic coordinates
    Integrates with Vehicle class for vehicle-specific speed calculations
    """
    
    # Traffic multipliers for different times of day
    TRAFFIC_MULTIPLIERS = {
        "light": 1.0,      # Late night, early morning
        "moderate": 1.0,   # Normal daytime
        "heavy": 1.0,      # Rush hours
        "peak": 1.0        # Peak rush hours
    }
    
    # Peak hours (24-hour format)
    PEAK_HOURS = [(7, 9), (17, 19)]  # 7-9 AM, 5-7 PM
    HEAVY_HOURS = [(6, 7), (9, 11), (16, 17), (19, 21)]  # Adjacent to peak hours
    
    @staticmethod
    def get_traffic_multiplier(current_time=None):
        """
        Get traffic multiplier based on current time
        
        Args:
            current_time: datetime object, defaults to current time
            
        Returns:
            Traffic multiplier (float)
        """
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        
        # Check for peak hours
        for start, end in ETACalculator.PEAK_HOURS:
            if start <= hour < end:
                return ETACalculator.TRAFFIC_MULTIPLIERS["peak"]
        
        # Check for heavy hours
        for start, end in ETACalculator.HEAVY_HOURS:
            if start <= hour < end:
                return ETACalculator.TRAFFIC_MULTIPLIERS["heavy"]
        
        # Light traffic (late night/early morning)
        if hour < 6 or hour >= 22:
            return ETACalculator.TRAFFIC_MULTIPLIERS["light"]
        
        # Moderate traffic (normal daytime)
        return ETACalculator.TRAFFIC_MULTIPLIERS["moderate"]
    
    @staticmethod
    def calculate_eta_for_vehicle(lat1, lng1, lat2, lng2, vehicle, include_traffic=True, current_time=None):
        """
        Calculate ETA for a specific vehicle using its speed and the distance between coordinates
        
        Args:
            lat1, lng1: Latitude and longitude of starting point
            lat2, lng2: Latitude and longitude of destination
            vehicle: Vehicle object with average_speed property
            include_traffic: Whether to include traffic calculations
            current_time: datetime object, defaults to current time
            
        Returns:
            Dictionary with comprehensive ETA information
        """
        try:
            # Calculate distance using DistanceCalculator
            distance_km = DistanceCalculator.calculate_distance_km(lat1, lng1, lat2, lng2)
            distance_miles = DistanceCalculator.calculate_distance_miles(lat1, lng1, lat2, lng2)
            
            if distance_km <= 0 or vehicle.average_speed <= 0:
                return {
                    "distance_km": 0,
                    "distance_miles": 0,
                    "eta_minutes": 0,
                    "eta_formatted": "Invalid route",
                    "arrival_time": None,
                    "vehicle_type": vehicle.vehicle_type,
                    "vehicle_name": vehicle.vehicle_name,
                    "vehicle_speed": vehicle.average_speed
                }
            
            # Calculate basic ETA using vehicle's average speed
            time_hours = distance_km / vehicle.average_speed
            basic_eta_minutes = time_hours * 60
            
            # Set current time
            if current_time is None:
                current_time = datetime.now()
            
            # Apply traffic if requested
            if include_traffic:
                traffic_multiplier = ETACalculator.get_traffic_multiplier(current_time)
                traffic_adjusted_minutes = basic_eta_minutes * traffic_multiplier
                traffic_condition = ETACalculator.get_traffic_condition(traffic_multiplier)
                delay_minutes = traffic_adjusted_minutes - basic_eta_minutes
                final_eta_minutes = traffic_adjusted_minutes
            else:
                traffic_multiplier = 1.0
                traffic_condition = "No Traffic Data"
                delay_minutes = 0
                final_eta_minutes = basic_eta_minutes
            
            # Calculate arrival time
            arrival_time = current_time + timedelta(minutes=final_eta_minutes)
            
            # Prepare comprehensive result
            result = {
                "distance_km": distance_km,
                "distance_miles": distance_miles,
                "distance_formatted": DistanceCalculator.format_distance(lat1, lng1, lat2, lng2),
                "basic_eta_minutes": basic_eta_minutes,
                "eta_minutes": final_eta_minutes,
                "eta_formatted": ETACalculator.format_eta_time(final_eta_minutes),
                "basic_eta_formatted": ETACalculator.format_eta_time(basic_eta_minutes),
                "arrival_time": arrival_time,
                "departure_time": current_time,
                "vehicle_type": vehicle.vehicle_type,
                "vehicle_name": vehicle.vehicle_name,
                "vehicle_speed": vehicle.average_speed,
                "vehicle_capacity": vehicle.capacity
            }
            
            # Add traffic-specific information if included
            if include_traffic:
                result.update({
                    "traffic_multiplier": traffic_multiplier,
                    "traffic_condition": traffic_condition,
                    "delay_minutes": delay_minutes,
                    "delay_formatted": ETACalculator.format_eta_time(delay_minutes) if delay_minutes > 0 else "No delay"
                })
            
            return result
            
        except Exception as e:
            print(f"Error calculating ETA for vehicle: {e}")
            return {
                "distance_km": 0,
                "distance_miles": 0,
                "eta_minutes": 0,
                "eta_formatted": "Error calculating ETA",
                "arrival_time": None,
                "vehicle_type": getattr(vehicle, 'vehicle_type', 'Unknown'),
                "vehicle_name": getattr(vehicle, 'vehicle_name', 'Unknown'),
                "vehicle_speed": getattr(vehicle, 'average_speed', 0)
            }
    
    @staticmethod
    def calculate_eta_for_all_vehicles(lat1, lng1, lat2, lng2, include_traffic=True, current_time=None):
        """
        Calculate ETA for all available vehicle types
        
        Args:
            lat1, lng1: Latitude and longitude of starting point
            lat2, lng2: Latitude and longitude of destination
            include_traffic: Whether to include traffic calculations
            current_time: datetime object, defaults to current time
            
        Returns:
            Dictionary with ETA information for each vehicle type
        """
        # Create instances of all vehicle types
        vehicles = [
            Car4Seater("Economy Car"),
            Car6Seater("Family Car"), 
            Minivan("Minivan"),
            Van("Van"),
            Motorcycle("Motorcycle")
        ]
        
        results = {}
        
        for vehicle in vehicles:
            eta_info = ETACalculator.calculate_eta_for_vehicle(
                lat1, lng1, lat2, lng2, vehicle, include_traffic, current_time
            )
            results[vehicle.vehicle_type] = eta_info
        
        return results
    
    @staticmethod
    def get_fastest_vehicle_option(lat1, lng1, lat2, lng2, include_traffic=True, current_time=None):
        """
        Get the vehicle option with the fastest ETA
        
        Args:
            lat1, lng1: Latitude and longitude of starting point
            lat2, lng2: Latitude and longitude of destination
            include_traffic: Whether to include traffic calculations
            current_time: datetime object, defaults to current time
            
        Returns:
            Dictionary with information about the fastest vehicle option
        """
        all_etas = ETACalculator.calculate_eta_for_all_vehicles(
            lat1, lng1, lat2, lng2, include_traffic, current_time
        )
        
        if not all_etas:
            return None
        
        # Find the vehicle with minimum ETA
        fastest_vehicle = min(all_etas.items(), key=lambda x: x[1]["eta_minutes"])
        
        return {
            "fastest_vehicle_type": fastest_vehicle[0],
            "fastest_eta_info": fastest_vehicle[1],
            "all_options": all_etas
        }
    
    @staticmethod
    def get_traffic_condition(multiplier):
        """Get traffic condition description based on multiplier"""
        if multiplier <= 1.0:
            return "Light Traffic 🟢"
        elif multiplier <= 1.0:
            return "Moderate Traffic 🟡"
        elif multiplier <= 1.0:
            return "Heavy Traffic 🟠"
        else:
            return "Peak Traffic 🔴"
    
    @staticmethod
    def format_eta_time(total_minutes):
        """
        Format ETA time into readable string
        
        Args:
            total_minutes: Time in minutes (float)
            
        Returns:
            Formatted time string
        """
        if total_minutes < 1:
            return "Less than 1 minute"
        elif total_minutes < 60:
            minutes = int(round(total_minutes))
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            
            if minutes == 0:
                return f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
    
    @staticmethod
    def format_arrival_time(arrival_time):
        """
        Format arrival time into readable string
        
        Args:
            arrival_time: datetime object
            
        Returns:
            Formatted arrival time string
        """
        if arrival_time is None:
            return "Unknown"
        
        return arrival_time.strftime("%I:%M %p")
    
    @staticmethod
    def get_comprehensive_eta_info(lat1, lng1, lat2, lng2, vehicle, include_traffic=True, current_time=None):
        """
        Get comprehensive ETA information with formatted display text
        
        Args:
            lat1, lng1: Latitude and longitude of starting point
            lat2, lng2: Latitude and longitude of destination
            vehicle: Vehicle object
            include_traffic: Whether to include traffic calculations
            current_time: datetime object, defaults to current time
            
        Returns:
            Dictionary with comprehensive ETA information and formatted text
        """
        eta_info = ETACalculator.calculate_eta_for_vehicle(
            lat1, lng1, lat2, lng2, vehicle, include_traffic, current_time
        )
        
        if eta_info["eta_minutes"] == 0:
            return eta_info
        
        # Create formatted display text
        display_parts = []
        
        # Basic info
        display_parts.append(f"🚗 {eta_info['vehicle_type']} ({eta_info['vehicle_name']})")
        display_parts.append(f"📏 Distance: {eta_info['distance_formatted']}")
        display_parts.append(f"⏱️ ETA: {eta_info['eta_formatted']}")
        display_parts.append(f"🏃 Speed: {eta_info['vehicle_speed']} km/h")
        
        if include_traffic and "traffic_condition" in eta_info:
            display_parts.append(f"🚦 {eta_info['traffic_condition']}")
            
            if eta_info.get("delay_minutes", 0) > 1:
                display_parts.append(f"⏰ Traffic Delay: +{eta_info['delay_formatted']}")
        
        if eta_info.get("arrival_time"):
            arrival_text = ETACalculator.format_arrival_time(eta_info["arrival_time"])
            display_parts.append(f"🎯 Arrival: {arrival_text}")
        
        eta_info["display_text"] = "\n".join(display_parts)
        eta_info["summary_text"] = f"{eta_info['eta_formatted']} via {eta_info['vehicle_type']}"
        
        return eta_info


# Utility functions for easy integration
def get_eta_for_vehicle_type(lat1, lng1, lat2, lng2, vehicle_type, include_traffic=True):
    """
    Simple function to get ETA for a specific vehicle type
    
    Args:
        lat1, lng1: Starting point coordinates
        lat2, lng2: Destination coordinates
        vehicle_type: String representing vehicle type (e.g., "Car4Seater", "Motorcycle")
        include_traffic: Whether to include traffic
        
    Returns:
        ETA information dictionary
    """
    # Create vehicle instance based on type
    vehicle_classes = {
        "Car4Seater": Car4Seater,
        "Car6Seater": Car6Seater,
        "Minivan": Minivan,
        "Van": Van,
        "Motorcycle": Motorcycle
    }
    
    if vehicle_type not in vehicle_classes:
        raise ValueError(f"Unknown vehicle type: {vehicle_type}")
    
    vehicle = vehicle_classes[vehicle_type](f"Default {vehicle_type}")
    
    return ETACalculator.calculate_eta_for_vehicle(
        lat1, lng1, lat2, lng2, vehicle, include_traffic
    )


def get_quick_eta(lat1, lng1, lat2, lng2, vehicle_type="Car4Seater", include_traffic=True):
    """
    Quick function to get just the ETA time and formatted string
    
    Args:
        lat1, lng1: Starting point coordinates
        lat2, lng2: Destination coordinates
        vehicle_type: Vehicle type string
        include_traffic: Whether to include traffic
        
    Returns:
        Tuple of (eta_minutes, eta_formatted_string)
    """
    result = get_eta_for_vehicle_type(lat1, lng1, lat2, lng2, vehicle_type, include_traffic)
    return result["eta_minutes"], result["eta_formatted"]


def get_arrival_time_for_vehicle(lat1, lng1, lat2, lng2, vehicle_type="Car4Seater", include_traffic=True):
    """
    Simple function to get estimated arrival time for a vehicle type
    
    Args:
        lat1, lng1: Starting point coordinates
        lat2, lng2: Destination coordinates
        vehicle_type: Vehicle type string
        include_traffic: Whether to include traffic
        
    Returns:
        datetime object of estimated arrival time
    """
    result = get_eta_for_vehicle_type(lat1, lng1, lat2, lng2, vehicle_type, include_traffic)
    return result.get("arrival_time")


def compare_vehicle_etas(lat1, lng1, lat2, lng2, include_traffic=True):
    """
    Compare ETAs across all vehicle types
    
    Args:
        lat1, lng1: Starting point coordinates
        lat2, lng2: Destination coordinates
        include_traffic: Whether to include traffic
        
    Returns:
        Dictionary with comparison data and sorted list of vehicles by ETA
    """
    all_etas = ETACalculator.calculate_eta_for_all_vehicles(lat1, lng1, lat2, lng2, include_traffic)
    
    # Sort by ETA time
    sorted_vehicles = sorted(all_etas.items(), key=lambda x: x[1]["eta_minutes"])
    
    return {
        "all_etas": all_etas,
        "sorted_by_speed": sorted_vehicles,
        "fastest": sorted_vehicles[0] if sorted_vehicles else None,
        "slowest": sorted_vehicles[-1] if sorted_vehicles else None
    }