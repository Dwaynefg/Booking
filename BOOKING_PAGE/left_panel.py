import customtkinter as ctk
from CALCULATIONS.distance_calculator import DistanceCalculator

class LeftPanel:
    """Manages the left panel components - map and location inputs"""
    
    def __init__(self, parent_frame, parent_app):
        self.parent_frame = parent_frame
        self.parent_app = parent_app
        
        # UI Components
        self.map_frame = None
        self.entry_1 = None  # Pickup entry
        self.entry_2 = None  # Dropoff entry
        self.distance_label = None
        
        # Location coordinates
        self.pickup_coordinates = None  # (lat, lng)
        self.dropoff_coordinates = None  # (lat, lng)
        
        self.setup_left_panel()

    def setup_left_panel(self):
        """Setup the left panel with map and inputs"""
        # Map container
        self.map_frame = ctk.CTkFrame(self.parent_frame, fg_color="#EEEEEE", border_width=1)
        self.map_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Location inputs section
        inputs_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=(0, 10))
        
        # Pickup location
        pickup_label = ctk.CTkLabel(inputs_frame, text="Pickup location:", font=ctk.CTkFont(size=12), text_color="#000000")
        pickup_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_1 = ctk.CTkEntry(inputs_frame, placeholder_text="Enter pickup address...", height=40, font=ctk.CTkFont(size=11), fg_color="#E8E8E8", corner_radius=25, border_width=0, text_color="#000000")
        self.entry_1.pack(fill="x", pady=(0, 15))
        
        # Dropoff location
        dropoff_label = ctk.CTkLabel(inputs_frame, text="Dropoff location:", font=ctk.CTkFont(size=12), text_color="#000000")
        dropoff_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_2 = ctk.CTkEntry(inputs_frame, placeholder_text="Enter dropoff address...", height=40, font=ctk.CTkFont(size=11), fg_color="#E8E8E8", corner_radius=25, border_width=0, text_color="#000000")
        self.entry_2.pack(fill="x")
        
        # Distance info
        self.distance_label = ctk.CTkLabel(inputs_frame, text="📍 Select pickup and dropoff locations", font=ctk.CTkFont(size=10), text_color="#666666")
        self.distance_label.pack(anchor="w", pady=(10, 0))

    def set_pickup_location(self, lat, lng, address=None):
        """Set pickup location coordinates"""
        self.pickup_coordinates = (lat, lng)
        if address and self.entry_1:
            self.set_entry_text(self.entry_1, address)
        self.update_distance_display()

    def set_dropoff_location(self, lat, lng, address=None):
        """Set dropoff location coordinates"""
        self.dropoff_coordinates = (lat, lng)
        if address and self.entry_2:
            self.set_entry_text(self.entry_2, address)
        self.update_distance_display()

    def update_distance_display(self):
        """Update the distance display"""
        try:
            if self.pickup_coordinates and self.dropoff_coordinates:
                pickup_lat, pickup_lng = self.pickup_coordinates
                dropoff_lat, dropoff_lng = self.dropoff_coordinates
                
                distance_text = DistanceCalculator.format_distance(
                    pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
                )
                self.distance_label.configure(
                    text=f"📏 Distance: {distance_text}", 
                    text_color="green"
                )
            else:
                self.distance_label.configure(
                    text="📍 Select pickup and dropoff locations", 
                    text_color="#666666"
                )
                
        except Exception as e:
            print(f"Error updating distance display: {e}")
            self.distance_label.configure(
                text="❌ Error calculating distance", 
                text_color="red"
            )

    def set_entry_text(self, entry, text):
        """Helper method to set entry text"""
        entry.delete(0, 'end')
        entry.insert(0, text)

    def reset_entries(self):
        """Reset entry fields and coordinates"""
        if self.entry_1:
            self.entry_1.delete(0, 'end')
        if self.entry_2:
            self.entry_2.delete(0, 'end')
        
        # Reset coordinates
        self.pickup_coordinates = None
        self.dropoff_coordinates = None
        
        # Reset distance display
        if self.distance_label:
            self.distance_label.configure(text="📍 Select pickup and dropoff locations")

    def get_pickup_text(self):
        """Get pickup entry text"""
        return self.entry_1.get() if self.entry_1 else ""
    
    def get_dropoff_text(self):
        """Get dropoff entry text"""
        return self.entry_2.get() if self.entry_2 else ""
    
    def get_pickup_coordinates(self):
        """Get pickup coordinates"""
        return self.pickup_coordinates
    
    def get_dropoff_coordinates(self):
        """Get dropoff coordinates"""
        return self.dropoff_coordinates