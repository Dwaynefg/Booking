import customtkinter
import tkinter as tk
from map_widget import MapWidget
from distance_calculator import DistanceCalculator

class LocationPickerApp:
    def __init__(self):
        customtkinter.set_appearance_mode("light")  
        customtkinter.set_default_color_theme("blue")
        
        self.root = customtkinter.CTk()
        self.root.geometry("1200x800")
        self.root.title("Location Picker")
        self.root.state('zoomed')
        self.root.minsize(800, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        main_container = customtkinter.CTkFrame(self.root)
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=0)
        main_container.grid_columnconfigure(0, weight=1)
        
        self.create_map_section(main_container)
        self.create_controls_section(main_container)
    
    def create_map_section(self, parent):
        """Create the map section"""
        map_container = customtkinter.CTkFrame(parent, border_color="black", border_width=2)
        map_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        map_container.grid_rowconfigure(0, weight=1)
        map_container.grid_columnconfigure(0, weight=1)
        
        self.map_widget = MapWidget(map_container, width=800, height=500, parent_app=self)
        self.map_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.create_map_type_selector(map_container)
    
    def create_controls_section(self, parent):
        """Create the controls section"""
        controls_container = customtkinter.CTkFrame(parent)
        controls_container.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        controls_container.grid_columnconfigure(0, weight=1)
        controls_container.grid_columnconfigure(1, weight=1)
        
        # Left column - Location selectors
        left_frame = customtkinter.CTkFrame(controls_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.create_location_selectors(left_frame)
        
        # Right column - Distance and instructions
        right_frame = customtkinter.CTkFrame(controls_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.create_distance_display(right_frame)
        self.create_instructions(right_frame)
    
    def create_map_type_selector(self, parent):
        """Create map type selector"""
        type_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        type_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        customtkinter.CTkLabel(type_frame, text="Map Type:", 
                              font=customtkinter.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))
        
        self.map_type_dropdown = customtkinter.CTkComboBox(
            type_frame, values=["Google Maps", "Satellite"], width=150,
            command=self.on_map_type_change, font=customtkinter.CTkFont(size=12))
        self.map_type_dropdown.set("Google Maps")
        self.map_type_dropdown.pack(side="left")
    
    def create_location_selector(self, parent, label_text, callback):
        """Create a location selector (pickup or dropoff)"""
        frame = customtkinter.CTkFrame(parent, border_width=1)
        frame.pack(fill="x", pady=(0, 10))
        frame.grid_columnconfigure(1, weight=1)
        
        customtkinter.CTkLabel(frame, text=label_text, 
                              font=customtkinter.CTkFont(size=14, weight="bold")).grid(
                                  row=0, column=0, padx=15, pady=15, sticky="w")
        
        dropdown = customtkinter.CTkComboBox(
            frame, values=self.map_widget.get_location_options(), 
            command=callback, font=customtkinter.CTkFont(size=12), height=35)
        dropdown.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        
        return dropdown
    
    def create_location_selectors(self, parent):
        """Create pickup and dropoff selectors"""
        customtkinter.CTkLabel(parent, text="Location Selection",
                              font=customtkinter.CTkFont(size=16, weight="bold")).pack(pady=(0, 15))
        
        self.pickup_dropdown = self.create_location_selector(
            parent, "Pickup:", self.map_widget.set_pickup_location)
        self.dropoff_dropdown = self.create_location_selector(
            parent, "Drop Off:", self.map_widget.set_dropoff_location)
    
    def create_distance_display(self, parent):
        """Create distance display section"""
        customtkinter.CTkLabel(parent, text="Distance Information",
                              font=customtkinter.CTkFont(size=16, weight="bold")).pack(pady=(0, 15))
        
        distance_frame = customtkinter.CTkFrame(parent, border_width=1)
        distance_frame.pack(fill="x", pady=(0, 15))
        distance_frame.grid_columnconfigure(1, weight=1)
        
        customtkinter.CTkLabel(distance_frame, text="Distance:",
                              font=customtkinter.CTkFont(size=14, weight="bold")).grid(
                                  row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.distance_label = customtkinter.CTkLabel(
            distance_frame, text="Select pickup and dropoff locations",
            font=customtkinter.CTkFont(size=13, weight="bold"), text_color="blue")
        self.distance_label.grid(row=0, column=1, padx=15, pady=15, sticky="w")
    
    def create_instructions(self, parent):
        """Create instruction text"""
        instructions = customtkinter.CTkLabel(
            parent, justify="left", font=customtkinter.CTkFont(size=12), text_color="gray",
            text="💡 Tip: Click anywhere on the map to set pickup/dropoff locations!\n"
                 "🗺️ Use the dropdown menus to select predefined locations\n"
                 "📏 Distance is calculated automatically when both locations are set")
        instructions.pack(pady=(0, 10))
    
    def update_distance_display(self):
        """Update the distance display using DistanceCalculator"""
        try:
            pickup_pos = self.map_widget.get_pickup_position()
            dropoff_pos = self.map_widget.get_dropoff_position()
            
            if pickup_pos and dropoff_pos:
                # Use DistanceCalculator to format the distance
                distance_text = DistanceCalculator.format_distance(
                    pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1])
                self.distance_label.configure(text=distance_text, text_color="green")
            else:
                self.distance_label.configure(text="Select pickup and dropoff locations", text_color="blue")
        except Exception as e:
            print(f"Error updating distance display: {e}")
            self.distance_label.configure(text="Error calculating distance", text_color="red")
    
    def create_dialog_button(self, parent, text, command, color, hover_color):
        """Create a dialog button with consistent styling"""
        return customtkinter.CTkButton(parent, text=text, command=command, 
                                     fg_color=color, hover_color=hover_color)
    
    def show_location_confirmation_dialog(self, lat, lng, address):
        """Show confirmation dialog for clicked location"""
        try:
            dialog = customtkinter.CTkToplevel(self.root)
            dialog.title("Set Location")
            dialog.geometry("400x200")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x, y = (dialog.winfo_screenwidth() - 400) // 2, (dialog.winfo_screenheight() - 200) // 2
            dialog.geometry(f"400x200+{x}+{y}")
            
            main_frame = customtkinter.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Labels
            customtkinter.CTkLabel(main_frame, text="Set Location Type",
                                 font=customtkinter.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
            customtkinter.CTkLabel(main_frame, text=f"Location: {address}",
                                 font=customtkinter.CTkFont(size=12), wraplength=350).pack(pady=(0, 15))
            customtkinter.CTkLabel(main_frame, text=f"Coordinates: {lat:.6f}, {lng:.6f}",
                                 font=customtkinter.CTkFont(size=10), text_color="gray").pack(pady=(0, 15))
            
            # Buttons
            button_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=(10, 0))
            
            pickup_btn = self.create_dialog_button(
                button_frame, "Set as Pickup", 
                lambda: self.set_clicked_location(dialog, lat, lng, address, "pickup"),
                "green", "darkgreen")
            pickup_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)
            
            dropoff_btn = self.create_dialog_button(
                button_frame, "Set as Drop Off",
                lambda: self.set_clicked_location(dialog, lat, lng, address, "dropoff"), 
                "red", "darkred")
            dropoff_btn.pack(side="left", padx=(10, 0), fill="x", expand=True)
            
            self.create_dialog_button(main_frame, "Cancel", dialog.destroy, 
                                    "gray", "darkgray").pack(pady=(10, 0))
            
        except Exception as e:
            print(f"Error creating location dialog: {e}")
    
    def set_clicked_location(self, dialog, lat, lng, address, location_type):
        """Set the clicked location as pickup or dropoff"""
        try:
            dialog.destroy()
            
            if location_type == "pickup":
                self.map_widget.set_custom_pickup_location(lat, lng, address)
                self.pickup_dropdown.set(f"{address}")
            else:
                self.map_widget.set_custom_dropoff_location(lat, lng, address)
                self.dropoff_dropdown.set(f"{address}")
        except Exception as e:
            print(f"Error setting clicked location: {e}")
    
    def on_map_type_change(self, choice):
        """Handle map type selection"""
        self.map_widget.set_map_type(choice)
    
    def get_distance_info(self):
        """Get current distance information"""
        pickup_pos = self.map_widget.get_pickup_position()
        dropoff_pos = self.map_widget.get_dropoff_position()
        
        if pickup_pos and dropoff_pos:
            distance_km = DistanceCalculator.calculate_distance_km(
                pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1])
            distance_miles = DistanceCalculator.calculate_distance_miles(
                pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1])
            
            return {
                'distance_km': distance_km,
                'distance_miles': distance_miles,
                'pickup_coordinates': pickup_pos,
                'dropoff_coordinates': dropoff_pos
            }
        return None
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LocationPickerApp()
    app.run()