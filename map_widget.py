import tkintermapview
import requests
import threading
from distance_calculator import DistanceCalculator

class MapWidget:
    def __init__(self, parent, width=400, height=300, parent_app=None):
        self.pickup_marker = None
        self.dropoff_marker = None
        self.parent_app = parent_app
        
        # Location coordinates (predefined locations)
        self.locations = {
            "PUP College of Engineering": (14.5991435, 121.00536490272962),
            "PUP Main Campus": (14.598996, 121.011711),
            "SM City Sta. Mesa": (14.604704, 121.018379)
        }
        
        # Create map widget
        self.map_widget = tkintermapview.TkinterMapView(parent, width=width, height=height, corner_radius=5)
        self.map_widget.set_position(14.5991435, 121.00536490272962)
        self.map_widget.set_zoom(15)
        
        # Set default map type to Google Maps
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        
        # Bind click event
        self.map_widget.add_left_click_map_command(self.on_map_click)
    
    def pack(self, **kwargs):
        self.map_widget.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.map_widget.grid(**kwargs)
    
    def on_map_click(self, coordinates_tuple):
        """Handle map click events"""
        try:
            lat, lng = coordinates_tuple
            threading.Thread(target=self.get_address_and_show_dialog, args=(lat, lng), daemon=True).start()
        except Exception as e:
            print(f"Error handling map click: {e}")
    
    def get_address_and_show_dialog(self, lat, lng):
        """Get address from coordinates and show confirmation dialog"""
        try:
            address = self.get_address_from_coordinates(lat, lng)
            if self.parent_app:
                self.parent_app.root.after(0, 
                    lambda: self.parent_app.show_location_confirmation_dialog(lat, lng, address))
        except Exception as e:
            print(f"Error getting address and showing dialog: {e}")
            if self.parent_app:
                fallback_address = f"Location at {lat:.4f}, {lng:.4f}"
                self.parent_app.root.after(0, 
                    lambda: self.parent_app.show_location_confirmation_dialog(lat, lng, fallback_address))
    
    def get_address_from_coordinates(self, lat, lng):
        """Convert coordinates to human-readable address using reverse geocoding"""
        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={'lat': lat, 'lon': lng, 'format': 'json', 'addressdetails': 1, 'zoom': 18},
                headers={'User-Agent': 'LocationPickerApp/1.0'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                address_data = data.get('address', {})
                
                # Build address from components
                address_parts = [
                    address_data.get('house_number', ''),
                    address_data.get('road', ''),
                    address_data.get('suburb') or address_data.get('neighbourhood', ''),
                    address_data.get('city') or address_data.get('town', '')
                ]
                
                # Filter out empty parts and join
                address_parts = [part for part in address_parts if part]
                return ', '.join(address_parts) if address_parts else data.get('display_name', f"Location at {lat:.4f}, {lng:.4f}")
            
        except Exception as e:
            print(f"Error getting address: {e}")
        
        return f"Location at {lat:.4f}, {lng:.4f}"
    
    def set_map_type(self, map_type):
        """Change map type"""
        try:
            tile_servers = {
                "Google Maps": "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                "Satellite": "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
            }
            
            if map_type in tile_servers:
                self.map_widget.set_tile_server(tile_servers[map_type], max_zoom=22)
                self._redraw_elements()
        except Exception as e:
            print(f"Error setting map type: {e}")
    
    def _redraw_elements(self):
        """Redraw markers after map type change"""
        try:
            # Store current state
            pickup_data = (self.pickup_marker.position, self.pickup_marker.text) if self.pickup_marker else None
            dropoff_data = (self.dropoff_marker.position, self.dropoff_marker.text) if self.dropoff_marker else None
            
            self._clear_all()
            
            # Recreate markers
            if pickup_data:
                self._create_pickup_marker(*pickup_data[0], pickup_data[1])
            if dropoff_data:
                self._create_dropoff_marker(*dropoff_data[0], dropoff_data[1])
        except Exception as e:
            print(f"Error redrawing elements: {e}")
    
    def _clear_all(self):
        """Clear all markers"""
        try:
            for marker in [self.pickup_marker, self.dropoff_marker]:
                if marker:
                    marker.delete()
            self.pickup_marker = self.dropoff_marker = None
        except Exception as e:
            print(f"Error clearing markers: {e}")
    
    def _create_marker(self, lat, lng, text, color_outside, color_circle):
        """Generic marker creation method"""
        try:
            return self.map_widget.set_marker(lat, lng, text=text, 
                                            marker_color_outside=color_outside, 
                                            marker_color_circle=color_circle)
        except Exception as e:
            print(f"Error creating marker: {e}")
            return None
    
    def _create_pickup_marker(self, lat, lng, text="Pickup"):
        """Create pickup marker"""
        self.pickup_marker = self._create_marker(lat, lng, text, "green", "darkgreen")
    
    def _create_dropoff_marker(self, lat, lng, text="Drop Off"):
        """Create dropoff marker"""
        self.dropoff_marker = self._create_marker(lat, lng, text, "red", "darkred")
    
    def _set_location_internal(self, lat, lng, text, is_pickup=True):
        """Internal method to set location (pickup or dropoff)"""
        try:
            # Clear old marker
            if is_pickup and self.pickup_marker:
                self.pickup_marker.delete()
            elif not is_pickup and self.dropoff_marker:
                self.dropoff_marker.delete()
            
            # Create new marker
            if is_pickup:
                self._create_pickup_marker(lat, lng, text)
                self.map_widget.set_position(lat, lng)
            else:
                self._create_dropoff_marker(lat, lng, text)
            
            # Center map if both markers exist
            if self.pickup_marker and self.dropoff_marker:
                self._center_on_both_markers()
            
            # Update distance in parent app
            if self.parent_app:
                self.parent_app.update_distance_display()
                
        except Exception as e:
            print(f"Error setting location internally: {e}")
    
    def set_pickup_location(self, location_name):
        """Set pickup location from dropdown"""
        if location_name in self.locations:
            lat, lng = self.locations[location_name]
            self._set_location_internal(lat, lng, "Pickup", is_pickup=True)
    
    def set_custom_pickup_location(self, lat, lng, address):
        """Set custom pickup location from map click"""
        display_address = address[:30] + "..." if len(address) > 30 else address
        self._set_location_internal(lat, lng, f"Pickup\n{display_address}", is_pickup=True)
    
    def set_dropoff_location(self, location_name):
        """Set dropoff location from dropdown"""
        if location_name in self.locations:
            lat, lng = self.locations[location_name]
            self._set_location_internal(lat, lng, "Drop Off", is_pickup=False)
    
    def set_custom_dropoff_location(self, lat, lng, address):
        """Set custom dropoff location from map click"""
        display_address = address[:30] + "..." if len(address) > 30 else address
        self._set_location_internal(lat, lng, f"Drop Off\n{display_address}", is_pickup=False)
    
    def _center_on_both_markers(self):
        """Center map to show both markers using DistanceCalculator"""
        if not (self.pickup_marker and self.dropoff_marker):
            return
            
        try:
            pickup_pos = self.pickup_marker.position
            dropoff_pos = self.dropoff_marker.position
            
            # Use DistanceCalculator to get center point and zoom level
            center_lat, center_lng = DistanceCalculator.get_center_point(
                pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1])
            
            zoom = DistanceCalculator.get_zoom_level_for_distance(
                pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1])
            
            self.map_widget.set_position(center_lat, center_lng)
            self.map_widget.set_zoom(zoom)
            
        except Exception as e:
            print(f"Error centering map: {e}")
    
    def get_location_options(self):
        """Get available locations"""
        return list(self.locations.keys())
    
    def get_position(self, marker):
        """Generic method to get marker position"""
        try:
            return marker.position if marker else None
        except Exception as e:
            print(f"Error getting position: {e}")
            return None
    
    def get_pickup_position(self):
        """Get pickup marker position"""
        return self.get_position(self.pickup_marker)
    
    def get_dropoff_position(self):
        """Get dropoff marker position"""
        return self.get_position(self.dropoff_marker)
    
    def add_location(self, name, lat, lng):
        """Add a new predefined location"""
        self.locations[name] = (lat, lng)
    
    def remove_location(self, name):
        """Remove a predefined location"""
        if name in self.locations:
            del self.locations[name]
    
    def get_all_locations(self):
        """Get all predefined locations"""
        return self.locations.copy()