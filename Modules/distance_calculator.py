import math

class DistanceCalculator:
    """Utility class for calculating distances between geographic coordinates"""
    
    EARTH_RADIUS_KM = 6371  # Earth radius in kilometers
    KM_TO_MILES = 0.621371  # Conversion factor from kilometers to miles
    
    @staticmethod
    def calculate_distance_km(lat1, lng1, lat2, lng2):
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lng1: Latitude and longitude of first point
            lat2, lng2: Latitude and longitude of second point
            
        Returns:
            Distance in kilometers
        """
        try:
            # Convert to radians
            lat1_rad, lng1_rad, lat2_rad, lng2_rad = map(math.radians, [lat1, lng1, lat2, lng2])
            
            # Haversine formula
            dlat = lat2_rad - lat1_rad
            dlng = lng2_rad - lng1_rad
            
            a = (math.sin(dlat/2)**2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2)
            
            distance_km = 2 * math.asin(math.sqrt(a)) * DistanceCalculator.EARTH_RADIUS_KM
            return distance_km
            
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return 0
    
    @staticmethod
    def calculate_distance_miles(lat1, lng1, lat2, lng2):
        """
        Calculate distance between two points in miles
        
        Args:
            lat1, lng1: Latitude and longitude of first point
            lat2, lng2: Latitude and longitude of second point
            
        Returns:
            Distance in miles
        """
        distance_km = DistanceCalculator.calculate_distance_km(lat1, lng1, lat2, lng2)
        return distance_km * DistanceCalculator.KM_TO_MILES
    
    @staticmethod
    def format_distance(lat1, lng1, lat2, lng2):
        """
        Calculate and format distance as a readable string
        
        Args:
            lat1, lng1: Latitude and longitude of first point
            lat2, lng2: Latitude and longitude of second point
            
        Returns:
            Formatted distance string (e.g., "5.23 km (3.25 miles)")
        """
        distance_km = DistanceCalculator.calculate_distance_km(lat1, lng1, lat2, lng2)
        distance_miles = distance_km * DistanceCalculator.KM_TO_MILES
        return f"{distance_km:.2f} km ({distance_miles:.2f} miles)"
    
    @staticmethod
    def get_zoom_level_for_distance(lat1, lng1, lat2, lng2):
        """
        Calculate appropriate zoom level based on distance between two points
        
        Args:
            lat1, lng1: Latitude and longitude of first point
            lat2, lng2: Latitude and longitude of second point
            
        Returns:
            Appropriate zoom level for map display
        """
        try:
            lat_diff = abs(lat1 - lat2)
            lng_diff = abs(lng1 - lng2)
            max_diff = max(lat_diff, lng_diff)
            
            # Define zoom levels based on coordinate differences
            zoom_levels = [
                (0.1, 10),   # Large difference -> zoom out
                (0.05, 12),  # Medium difference
                (0.01, 14),  # Small difference
            ]
            
            # Find appropriate zoom level
            for threshold, zoom in zoom_levels:
                if max_diff > threshold:
                    return zoom
            
            return 15  # Default zoom for very close points
            
        except Exception as e:
            print(f"Error calculating zoom level: {e}")
            return 15  # Default zoom level
    
    @staticmethod
    def get_center_point(lat1, lng1, lat2, lng2):
        """
        Calculate the center point between two coordinates
        
        Args:
            lat1, lng1: Latitude and longitude of first point
            lat2, lng2: Latitude and longitude of second point
            
        Returns:
            Tuple of (center_lat, center_lng)
        """
        try:
            center_lat = (lat1 + lat2) / 2
            center_lng = (lng1 + lng2) / 2
            return (center_lat, center_lng)
        except Exception as e:
            print(f"Error calculating center point: {e}")
            return (lat1, lng1)  # Return first point as fallback