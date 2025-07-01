from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from DriverManager import DriverManager  # Import DriverManager

# Import the refactored modules
from map_widget import MapWidget
from distance_calculator import DistanceCalculator
from ui_manager import UIManager
from fare_calculation import FareCalculator

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Get the directory where this script is located
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def create_assets_folder():
    """Create assets folder if it doesn't exist"""
    ASSETS_PATH.mkdir(parents=True, exist_ok=True)

class IntegratedRideBookingApp:
    def __init__(self):
        self.window = None
        self.map_widget = None
        self.ui_manager = None
        self.selected_vehicle = None
        
        # Initialize DriverManager
        self.driver_manager = DriverManager("drivers.csv")  # Path to your driver CSV file
        
        # Use FareCalculator for vehicle data instead of local definition
        self.vehicle_data = FareCalculator.get_vehicle_data()
        
        self.setup_window()
        self.setup_components()
        
    def setup_window(self):
        """Setup the main window"""
        create_assets_folder()
    
        self.window = ctk.CTk()
        self.window.title("Go-do - Modern Ride Booking App")
        self.window.attributes('-fullscreen', True)
        self.window.state('zoomed')
    
        # Bind keyboard shortcuts
        self.window.bind('<F11>', self.toggle_fullscreen)
        self.window.bind('<Escape>', self.exit_fullscreen)
        self.window.bind('<Alt-Return>', self.toggle_fullscreen)
        
    def setup_components(self):
        """Setup UI components and map widget"""
        # Create UI Manager and pass DriverManager
        self.ui_manager = UIManager(self.window, self, self.driver_manager)
        
        # Create map widget
        self.map_widget = MapWidget(self.ui_manager.map_frame, parent_app=self)
        self.map_widget.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initial setup
        self.window.after(100, self.ui_manager.initial_resize)
        
    def button_click(self, button_name):
        """Handle button clicks"""
        if button_name == "book_ride":
            self.handle_book_ride()
        elif button_name == "cancel":
            self.reset_form()
        else:
            # Vehicle selection
            self.handle_vehicle_selection(button_name)
    
    def handle_book_ride(self):
        """Handle ride booking and assign a driver."""
        pickup = self.ui_manager.entry_1.get()
        dropoff = self.ui_manager.entry_2.get()

        if pickup and dropoff and pickup != "Enter pickup address..." and dropoff != "Enter dropoff address...":
            
            # Get fare breakdown using FareCalculator
            fare_data = self.get_current_fare_data()
            fare_breakdown = FareCalculator.format_fare_breakdown(fare_data)

            distance_text = self.ui_manager.distance_label.cget("text")
            vehicle_text = f"Vehicle: {self.selected_vehicle}" if self.selected_vehicle else "Vehicle: Not selected"

            # Select a driver based on the selected vehicle type
            selected_driver = self.driver_manager.get_driver_info(self.selected_vehicle)

            if selected_driver:
                driver_name = selected_driver['driver_name']
                driver_vehicle = selected_driver['vehicle_name']
                driver_contact = selected_driver['contact_no']
                driver_plate = selected_driver['plate_no']

                # Mark the driver as "busy" and save the changes to the CSV
                self.driver_manager.update_driver_status(self.selected_vehicle, driver_name, 'busy')

                # Create driver info dictionary
                driver_info = {
                    "driver_name": driver_name,
                    "vehicle_name": driver_vehicle,
                    "contact_no": driver_contact,
                    "plate_no": driver_plate
                }

                # Update driver info in the UI
                self.ui_manager.update_driver_info(driver_info)

                # Show booking confirmation popup
                messagebox.showinfo(
                    "Ride Booked Successfully! 🚗",
                    f"Ride booked successfully!\n\n"
                    f"📍 From: {pickup}\n"
                    f"📍 To: {dropoff}\n"
                    f"🚙 {vehicle_text}\n"
                    f"{distance_text}\n\n"
                    f"💰 Fare Breakdown:\n{fare_breakdown}"
                )
            else:
                messagebox.showwarning("No Available Driver", "Sorry, no available drivers for the selected vehicle type.")

        else:
            messagebox.showwarning("Missing Information ⚠️", "Please enter both pickup and dropoff locations")

        
    def handle_vehicle_selection(self, vehicle_name):
        """Handle vehicle selection"""
        if FareCalculator.is_valid_vehicle(vehicle_name):
            self.selected_vehicle = vehicle_name
            self.update_price_display()
            
            # Update UI to show selection
            self.ui_manager.update_vehicle_selection(vehicle_name)
            
            # Removed the messagebox popup - vehicle selection now happens silently
            print(f"Vehicle selected: {vehicle_name}")  # Optional: keep for debugging
        else:
            print(f"Vehicle {vehicle_name} not found in vehicle_data")
    
    def get_current_fare_data(self):
        """Get current fare data based on selections"""
        try:
            if not self.selected_vehicle:
                return None
            
            # Get coordinates
            pickup_coords = None
            dropoff_coords = None
            
            if self.map_widget:
                pickup_pos = self.map_widget.get_pickup_position()
                dropoff_pos = self.map_widget.get_dropoff_position()
                
                if pickup_pos:
                    pickup_coords = pickup_pos
                if dropoff_pos:
                    dropoff_coords = dropoff_pos
            
            # Get payment method
            payment_method = self.ui_manager.payment_mode.get()
            
            # Calculate fare
            return FareCalculator.calculate_final_fare(
                vehicle_name=self.selected_vehicle,
                payment_method=payment_method,
                pickup_coords=pickup_coords,
                dropoff_coords=dropoff_coords
            )
            
        except Exception as e:
            print(f"Error getting current fare data: {e}")
            return None
    
    def reset_form(self):
        """Reset the form to initial state"""
        self.ui_manager.reset_entries()
        
        # Clear map markers
        if self.map_widget:
            self.map_widget._clear_all()
        
        # Reset selections
        self.selected_vehicle = None
        self.update_price_display()
        self.update_distance_display()
        
        # Reset UI selections
        self.ui_manager.reset_vehicle_selection()
    
    def update_price_display(self):
        """Update price display based on selected vehicle and distance"""
        try:
            if not self.selected_vehicle:
                self.ui_manager.price_label.configure(text="0 pesos")
                return
            
            fare_data = self.get_current_fare_data()
            if fare_data:
                final_price = fare_data['final_total']
                self.ui_manager.price_label.configure(text=f"{final_price} pesos")
            else:
                # Fallback to base price
                base_price = FareCalculator.get_vehicle_base_price(self.selected_vehicle)
                self.ui_manager.price_label.configure(text=f"{base_price} pesos")
                
        except Exception as e:
            print(f"Error updating price display: {e}")
            if self.selected_vehicle:
                base_price = FareCalculator.get_vehicle_base_price(self.selected_vehicle)
                self.ui_manager.price_label.configure(text=f"{base_price} pesos")
            else:
                self.ui_manager.price_label.configure(text="0 pesos")
    
    def update_distance_display(self):
        """Update the distance display"""
        try:
            if not self.map_widget:
                return
                
            pickup_pos = self.map_widget.get_pickup_position()
            dropoff_pos = self.map_widget.get_dropoff_position()
            
            if pickup_pos and dropoff_pos:
                distance_text = DistanceCalculator.format_distance(
                    pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1]
                )
                self.ui_manager.distance_label.configure(
                    text=f"📏 Distance: {distance_text}", 
                    text_color="green"
                )
            else:
                self.ui_manager.distance_label.configure(
                    text="📍 Select pickup and dropoff locations", 
                    text_color="#666666"
                )
                
        except Exception as e:
            print(f"Error updating distance display: {e}")
            self.ui_manager.distance_label.configure(
                text="❌ Error calculating distance", 
                text_color="red"
            )
    
    def show_location_confirmation_dialog(self, lat, lng, address):
        """Show custom confirmation dialog with colored buttons"""
        try:
            # Create custom dialog window
            dialog = ctk.CTkToplevel(self.window)
            dialog.title("📍 Set Location")
            dialog.geometry("400x250")
            dialog.transient(self.window)
            dialog.grab_set()
            
            # Center the dialog
            dialog.geometry("+%d+%d" % (
                self.window.winfo_rootx() + 50,
                self.window.winfo_rooty() + 50
            ))
            
            # Main frame
            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = ctk.CTkLabel(
                main_frame,
                text="Set this location?",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=(10, 15))
            
            # Address
            address_label = ctk.CTkLabel(
                main_frame,
                text=f"📍 {address[:60]}{'...' if len(address) > 60 else ''}",
                font=ctk.CTkFont(size=12),
                wraplength=350
            )
            address_label.pack(pady=(0, 10))
            
            # Coordinates
            coord_label = ctk.CTkLabel(
                main_frame,
                text=f"🌐 {lat:.6f}, {lng:.6f}",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            coord_label.pack(pady=(0, 20))
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(10, 0))
            
            # Pickup button (Green)
            pickup_btn = ctk.CTkButton(
                buttons_frame,
                text="🚗 Pickup",
                fg_color="#4CAF50",
                hover_color="#45A049",
                width=100,
                height=40,
                command=lambda: self.handle_dialog_choice(dialog, lat, lng, address, "pickup")
            )
            pickup_btn.pack(side="left", padx=(0, 10))
            
            # Dropoff button (Red)
            dropoff_btn = ctk.CTkButton(
                buttons_frame,
                text="🏁 Dropoff",
                fg_color="#F44336",
                hover_color="#D32F2F", 
                width=100,
                height=40,
                command=lambda: self.handle_dialog_choice(dialog, lat, lng, address, "dropoff")
            )
            dropoff_btn.pack(side="left", padx=(0, 10))
            
            # Cancel button
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Cancel",
                fg_color="gray",
                hover_color="darkgray",
                width=80,
                height=40,
                command=dialog.destroy
            )
            cancel_btn.pack(side="right")
            
        except Exception as e:
            print(f"Error creating location dialog: {e}")
    
    def handle_dialog_choice(self, dialog, lat, lng, address, location_type):
        """Handle dialog button choice"""
        try:
            dialog.destroy()
            self.set_clicked_location(lat, lng, address, location_type)
        except Exception as e:
            print(f"Error handling dialog choice: {e}")
    
    def set_clicked_location(self, lat, lng, address, location_type):
        """Set the clicked location as pickup or dropoff"""
        try:
            shortened_address = address[:50] + "..." if len(address) > 50 else address
            
            if location_type == "pickup":
                if self.map_widget:
                    self.map_widget.set_custom_pickup_location(lat, lng, address)
                self.ui_manager.set_entry_text(self.ui_manager.entry_1, shortened_address)
            else:
                if self.map_widget:
                    self.map_widget.set_custom_dropoff_location(lat, lng, address)
                self.ui_manager.set_entry_text(self.ui_manager.entry_2, shortened_address)
            
            # Update displays
            self.update_distance_display()
            self.update_price_display()
            
        except Exception as e:
            print(f"Error setting clicked location: {e}")
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        current_state = self.window.attributes('-fullscreen')
        self.window.attributes('-fullscreen', not current_state)
        self.window.after(200, self.ui_manager.resize_components)
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.window.attributes('-fullscreen', False)
        self.window.after(200, self.ui_manager.resize_components)
    
    def show_controls_info(self):
        """Show controls information"""
        messagebox.showinfo("🎮 Controls & Features", 
            "🔧 Fullscreen Controls:\n\n" +
            "• F11 - Toggle fullscreen\n" +
            "• Alt+Enter - Toggle fullscreen\n" +
            "• Escape - Exit fullscreen\n\n" +
            "🗺️ Map Controls:\n" +
            "• Click on map to set pickup/dropoff\n" +
            "• Select vehicle type for pricing\n")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
        # Show feedback
        messagebox.showinfo("🎨 Theme Changed", f"Switched to {new_mode} mode!")
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = IntegratedRideBookingApp()
    app.run()
