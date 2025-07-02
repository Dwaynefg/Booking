import customtkinter as ctk
from tkinter import StringVar
from PIL import Image
from CALCULATIONS.fare_calculation import FareCalculator
import os
from BOOKING_PAGE.left_panel import LeftPanel
from BOOKING_PAGE.right_panel import RightPanel

class UIManager:
    """Manages all UI components and layout for the ride booking app"""
    
    def __init__(self, window, parent_app, driver_manager):
        self.window = window
        self.parent_app = parent_app
        self.driver_manager = driver_manager
        
        # Initialize panels
        self.left_panel = None
        self.right_panel = None
        
        # Track last window size
        self.last_window_size = (0, 0)
        
        # Initialize UI components
        self.main_frame = None
        self.help_button = None
        
        self.setup_ui_components()

    def setup_ui_components(self):
        """Setup all UI components"""
        # Create main container frame
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#F5F5F5", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Create header
        self.create_header()
    
        # Create content area with two panels
        self.create_content_panels()
        
        # Initialize left and right panels
        self.left_panel = LeftPanel(self.left_panel_frame, self.parent_app)
        self.right_panel = RightPanel(self.right_panel_frame, self.parent_app, self.driver_manager)

    def create_header(self):
        """Create the header with Go-Do branding and logo"""
        header_frame = ctk.CTkFrame(self.main_frame, height=60, fg_color="#520000", corner_radius=0)
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)

        # Create a container for logo and text
        logo_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_container.pack(side="left", padx=20, pady=10)

        try:
            # Load and resize the logo image
            logo_path = os.path.join("assets", "image_1.png")
            if os.path.exists(logo_path):
                # Load the image
                logo_image = Image.open(logo_path)
            
                # Resize to fit header (maintain aspect ratio)
                logo_height = 40
                aspect_ratio = logo_image.width / logo_image.height
                logo_width = int(logo_height * aspect_ratio)
                logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
                # Create CTk image
                logo_ctk = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(logo_width, logo_height))
            
                # Create logo label
                logo_label = ctk.CTkLabel(logo_container, image=logo_ctk, text="")
                logo_label.pack(side="left")
            else:
                # Fallback: Use text-based logo if image not found
                title_label = ctk.CTkLabel(logo_container, text="Go-Do", 
                                     font=ctk.CTkFont(family="Arial", size=28, weight="bold"), 
                                     text_color="white")
                title_label.pack(side="left")
            
        except Exception as e:
            # Fallback: Use text-based logo if image loading fails
            print(f"Could not load logo image: {e}")
            title_label = ctk.CTkLabel(logo_container, text="Go-Do", 
                                    font=ctk.CTkFont(family="Arial", size=28, weight="bold"), 
                                    text_color="white")
            title_label.pack(side="left")

        # Help button
        self.help_button = ctk.CTkButton(header_frame, text="?", width=30, height=30, 
                                        font=ctk.CTkFont(size=16, weight="bold"), 
                                        fg_color="#FFFFFF", text_color="#610C09", 
                                        hover_color="#E0E0E0", 
                                        command=self.parent_app.show_controls_info)
        self.help_button.pack(side="right", padx=20, pady=15)
    
    def create_content_panels(self):
        """Create left and right content panels"""
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        # Left panel for map and inputs
        self.left_panel_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.left_panel_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
        # Vertical divider
        divider = ctk.CTkFrame(content_frame, width=2, fg_color="#520000")
        divider.pack(side="left", fill="y", padx=5)
    
        # Right panel for vehicle selection and info
        self.right_panel_frame = ctk.CTkFrame(content_frame, width=500, fg_color="transparent")
        self.right_panel_frame.pack(side="right", fill="y", padx=(5, 0))
        self.right_panel_frame.pack_propagate(False)

    # Delegate methods to left panel
    def set_pickup_location(self, lat, lng, address=None):
        """Set pickup location coordinates"""
        self.left_panel.set_pickup_location(lat, lng, address)
        self.right_panel.set_location_coordinates(
            self.left_panel.get_pickup_coordinates(),
            self.left_panel.get_dropoff_coordinates()
        )

    def set_dropoff_location(self, lat, lng, address=None):
        """Set dropoff location coordinates"""
        self.left_panel.set_dropoff_location(lat, lng, address)
        self.right_panel.set_location_coordinates(
            self.left_panel.get_pickup_coordinates(),
            self.left_panel.get_dropoff_coordinates()
        )

    def get_pickup_text(self):
        """Get pickup entry text"""
        return self.left_panel.get_pickup_text()
    
    def get_dropoff_text(self):
        """Get dropoff entry text"""
        return self.left_panel.get_dropoff_text()
    
    def get_pickup_coordinates(self):
        """Get pickup coordinates"""
        return self.left_panel.get_pickup_coordinates()
    
    def get_dropoff_coordinates(self):
        """Get dropoff coordinates"""
        return self.left_panel.get_dropoff_coordinates()

    # Delegate methods to right panel
    def get_selected_vehicle(self):
        """Get currently selected vehicle"""
        return self.right_panel.get_selected_vehicle()
    
    def get_selected_vehicle_price(self):
        """Get currently selected vehicle price"""
        return self.right_panel.get_selected_vehicle_price()
    
    def get_payment_mode(self):
        """Get selected payment mode"""
        return self.right_panel.get_payment_mode()
    
    def get_current_fare_info(self):
        """Get current fare information"""
        return self.right_panel.get_current_fare_info()

    def get_fare_breakdown(self):
        """Get detailed fare breakdown for display"""
        return self.right_panel.get_fare_breakdown()

    def reset_entries(self):
        """Reset entry fields and coordinates"""
        self.left_panel.reset_entries()
        self.right_panel.reset_vehicle_selection()

    def initial_resize(self):
        """Initial resize after window creation"""
        self.resize_components()
        
    def resize_components(self):
        """Resize components based on window size"""
        # This method can be expanded if needed for responsive design
        pass