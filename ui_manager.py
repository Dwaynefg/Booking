import customtkinter as ctk
from tkinter import StringVar
import random

class UIManager:
    """Manages all UI components and layout for the ride booking app"""
    
    def __init__(self, window, parent_app, driver_manager):
        self.window = window
        self.parent_app = parent_app
        self.driver_manager = driver_manager  # Store the DriverManager instance
        self.last_window_size = (0, 0)
        self.resize_job_id = None
        
        # Payment mode variable
        self.payment_mode = StringVar(value="Cash")
        
        # UI Components
        self.main_frame = None
        self.left_panel = None
        self.right_panel = None
        self.map_frame = None
        self.entry_1 = None
        self.entry_2 = None
        self.distance_label = None
        self.price_label = None
        self.help_button = None
        self.vehicle_buttons = []
        self.action_buttons = []
        self.payment_radio_buttons = []
        
        # Driver info components
        self.driver_name_value = ctk.CTkLabel(self.window, text="Not assigned")
        self.plate_value = ctk.CTkLabel(self.window, text="N/A")
        self.vehicle_value = ctk.CTkLabel(self.window, text="N/A")
        self.contact_value = ctk.CTkLabel(self.window, text="N/A")
        
        self.setup_ui_components()
        self.setup_event_bindings()
    
    def setup_ui_components(self):
        """Setup all UI components"""
        # Create main container frame
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#F5F5F5", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Create header
        self.create_header()
    
        # Create content area with two panels
        self.create_content_panels()
    
        # Setup left panel (map and inputs)
        self.setup_left_panel()
    
        # Setup right panel (vehicle selection, driver info, payment)
        self.setup_right_panel()
    
    def create_header(self):
        """Create the header with Go-do branding"""
        header_frame = ctk.CTkFrame(
            self.main_frame, 
            height=60,
            fg_color="#520000",
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)
    
        # Go-do title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Go-do",
            font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=15)
    
        # Help button
        self.help_button = ctk.CTkButton(
            header_frame,
            text="?",
            width=30,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#FFFFFF",
            text_color="#520000",
            hover_color="#E0E0E0",
            command=self.parent_app.show_controls_info
        )
        self.help_button.pack(side="right", padx=20, pady=15)
    
    def create_content_panels(self):
        """Create left and right content panels"""
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        # Left panel for map and inputs
        self.left_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
        # Vertical divider
        divider = ctk.CTkFrame(content_frame, width=2, fg_color="#520000")
        divider.pack(side="left", fill="y", padx=5)
    
        # Right panel for vehicle selection and info
        self.right_panel = ctk.CTkFrame(content_frame, width=500, fg_color="transparent")
        self.right_panel.pack(side="right", fill="y", padx=(5, 0))
        self.right_panel.pack_propagate(False)
    
    def setup_left_panel(self):
        """Setup the left panel with map and inputs"""
        # Map container
        self.map_frame = ctk.CTkFrame(self.left_panel, fg_color="#EEEEEE", border_width=1)
        self.map_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Location inputs section
        inputs_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=(0, 10))
        
        # Pickup location
        pickup_label = ctk.CTkLabel(
            inputs_frame,
            text="Pickup location:",
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        )
        pickup_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_1 = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Enter pickup address...",
            height=40,
            font=ctk.CTkFont(size=11),
            fg_color="#E8E8E8",
            corner_radius=25,
            border_width=0,
            text_color="#000000"
        )
        self.entry_1.pack(fill="x", pady=(0, 15))
        
        # Dropoff location
        dropoff_label = ctk.CTkLabel(
            inputs_frame,
            text="Dropoff location:",
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        )
        dropoff_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_2 = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Enter dropoff address...",
            height=40,
            font=ctk.CTkFont(size=11),
            fg_color="#E8E8E8",
            corner_radius=25,
            border_width=0,
            text_color="#000000"
        )
        self.entry_2.pack(fill="x")
        
        # Distance info
        self.distance_label = ctk.CTkLabel(
            inputs_frame,
            text="📍 Select pickup and dropoff locations",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        self.distance_label.pack(anchor="w", pady=(10, 0))
    
    def setup_right_panel(self):
        """Setup the right panel with vehicle selection, driver info, and payment"""
        # Vehicle selection section
        self.create_vehicle_selection()
        
        # Driver information section  
        self.create_driver_info()
        
        # Payment section
        self.create_payment_section()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_vehicle_selection(self):
        """Create vehicle selection section"""
        vehicle_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        vehicle_frame.pack(fill="x", pady=(0, 20))
        
        # Section title
        title_label = ctk.CTkLabel(
            vehicle_frame,
            text="Select Vehicle Type",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Vehicle buttons
        vehicles = [
            ("Car(4 Seater)", "₱ 100.00"),
            ("Car(6 Seater)", "₱ 120.00"), 
            ("Mini Van", "₱ 200.00"),
            ("Van", "₱ 250.00"),
            ("Motorcycle", "₱ 50.00")
        ]
        
        self.vehicle_buttons = []
        for vehicle_name, price in vehicles:
            btn_frame = ctk.CTkFrame(vehicle_frame, fg_color="#E8E8E8", height=45)
            btn_frame.pack(fill="x", pady=2)
            btn_frame.pack_propagate(False)
            
            # Vehicle icon (circle)
            icon_frame = ctk.CTkFrame(btn_frame, width=30, height=30, fg_color="#9C9C9C", corner_radius=15)
            icon_frame.pack(side="left", padx=(15, 10), pady=7)
            icon_frame.pack_propagate(False)
            
            # Vehicle name
            name_label = ctk.CTkLabel(
                btn_frame,
                text=vehicle_name,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            )
            name_label.pack(side="left", pady=12)
            
            # Price
            price_label = ctk.CTkLabel(
                btn_frame,
                text=price,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            )
            price_label.pack(side="right", padx=15, pady=12)
            
            # Make the frame clickable - FIXED: Use the full vehicle name instead of splitting
            btn_frame.bind("<Button-1>", lambda e, v=vehicle_name: self.parent_app.button_click(v))
            icon_frame.bind("<Button-1>", lambda e, v=vehicle_name: self.parent_app.button_click(v))
            name_label.bind("<Button-1>", lambda e, v=vehicle_name: self.parent_app.button_click(v))
            price_label.bind("<Button-1>", lambda e, v=vehicle_name: self.parent_app.button_click(v))
            
            self.vehicle_buttons.append((btn_frame, icon_frame, vehicle_name))

    
    def create_driver_info(self):
        """Create driver information section if it doesn't exist, or just update it."""
        # Create the frame only if it doesn't exist
        if not hasattr(self, 'driver_frame'):
            self.driver_frame = ctk.CTkFrame(self.right_panel, fg_color="#F5F5F5", border_width=1, border_color="#CCCCCC")
            self.driver_frame.pack(fill="x", pady=(0, 20))

            # Section title
            title_label = ctk.CTkLabel(
                self.driver_frame,
                text="Driver's Information:",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#000000"
            )
            title_label.pack(anchor="w", padx=15, pady=(15, 10))

            # Driver details frame
            details_frame = ctk.CTkFrame(self.driver_frame, fg_color="transparent")
            details_frame.pack(fill="x", padx=15, pady=(0, 15))

            # Left column
            left_col = ctk.CTkFrame(details_frame, fg_color="transparent")
            left_col.pack(side="left", fill="both", expand=True)

            # Driver Name Label
            self.driver_name_label = ctk.CTkLabel(
                left_col,
                text="Driver Name",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#000000"
            )
            self.driver_name_label.pack(anchor="w")

            # Driver Name Value
            self.driver_name_value = ctk.CTkLabel(
                left_col,
                text="N/A",  # Default value
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#000000"
            )
            self.driver_name_value.pack(anchor="w", pady=(5, 0))

            # Plate Number Label
            plate_label = ctk.CTkLabel(
                left_col,
                text="Plate Number:",
                font=ctk.CTkFont(size=10),
                text_color="#666666"
            )
            plate_label.pack(anchor="w", pady=(5, 0))

            # Plate Number Value
            self.plate_value = ctk.CTkLabel(
                left_col,
                text="N/A",  # Default value
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#000000"
            )
            self.plate_value.pack(anchor="w")

            # Right column  
            right_col = ctk.CTkFrame(details_frame, fg_color="transparent")
            right_col.pack(side="right", fill="both", expand=True)

            # Vehicle Description Label
            vehicle_desc_label = ctk.CTkLabel(
                right_col,
                text="Vehicle Description",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#000000"
            )
            vehicle_desc_label.pack(anchor="w")

            # Vehicle Description Value
            self.vehicle_desc_value = ctk.CTkLabel(
                right_col,
                text="N/A",  # Default value
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#000000"
            )
            self.vehicle_desc_value.pack(anchor="w", pady=(5, 0))

            # Contact Number Label
            contact_label = ctk.CTkLabel(
                right_col,
                text="Contact Number:",
                font=ctk.CTkFont(size=10),
                text_color="#666666"
            )
            contact_label.pack(anchor="w", pady=(5, 0))

            # Contact Number Value
            self.contact_value = ctk.CTkLabel(
                right_col,
                text="N/A",  # Default value
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#000000"
            )
            self.contact_value.pack(anchor="w")

    def update_driver_info(self, driver_info):
        """Update the displayed driver information"""
        try:
            # Update the labels with the new driver information
            self.driver_name_value.configure(text=driver_info.get("driver_name", "N/A"))
            self.plate_value.configure(text=driver_info.get("plate_no", "N/A"))
            self.vehicle_desc_value.configure(text=driver_info.get("vehicle_name", "N/A"))
            self.contact_value.configure(text=driver_info.get("contact_no", "N/A"))
        except Exception as e:
            print(f"Error updating driver information: {e}")


    
    def create_payment_section(self):
        """Create payment mode selection section"""
        payment_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        payment_frame.pack(fill="x", pady=(0, 20))
        
        # Price display
        price_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=(0, 15))
        
        price_text_label = ctk.CTkLabel(
            price_frame,
            text="Price:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        )
        price_text_label.pack(side="left")
        
        self.price_label = ctk.CTkLabel(
            price_frame,
            text="0 Pesos",
            font=ctk.CTkFont(size=36),
            text_color="#808080"
        )
        self.price_label.pack(side="left", padx=(10, 0))
        
        # Payment mode selection
        payment_mode_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
        payment_mode_frame.pack(fill="x")
        
        mode_title = ctk.CTkLabel(
            payment_mode_frame,
            text="Select Mode of Payment",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        )
        mode_title.pack(anchor="w", pady=(0, 10))
        
        # Payment options
        payment_options_frame = ctk.CTkFrame(payment_mode_frame, fg_color="transparent")
        payment_options_frame.pack(fill="x")
        
        # Cash option
        cash_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Cash",
            variable=self.payment_mode,
            value="Cash",
            font=ctk.CTkFont(size=11),
            text_color="#000000"
        )
        cash_radio.pack(anchor="w", pady=2)
        
        # Online Payment option
        online_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Online Payment",
            variable=self.payment_mode,
            value="Online Payment", 
            font=ctk.CTkFont(size=11),
            text_color="#000000"
        )
        online_radio.pack(anchor="w", pady=2)
        
        self.payment_radio_buttons = [cash_radio, online_radio]
    
    def create_action_buttons(self):
        """Create Cancel and Confirm buttons"""
        buttons_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom")
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#DC5F5F",
            hover_color="#C54545",
            command=lambda: self.parent_app.button_click("cancel")
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # Confirm button  
        confirm_button = ctk.CTkButton(
            buttons_frame,
            text="Confirm",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049",
            command=lambda: self.parent_app.button_click("book_ride")
        )
        confirm_button.pack(side="right")
        
        self.action_buttons = [cancel_button, confirm_button]
    
    def setup_event_bindings(self):
        """Setup event bindings for window resize"""
        self.window.bind('<Configure>', self.on_window_configure)
    
    def set_entry_text(self, entry, text):
        """Set text in entry field"""
        entry.delete(0, 'end')
        entry.insert(0, text)
    
    def reset_entries(self):
        """Reset entry fields to placeholder state"""
        self.entry_1.delete(0, 'end')
        self.entry_2.delete(0, 'end')
        
        # Reset labels
        self.distance_label.configure(text="📍 Select pickup and dropoff locations")
    
    def update_vehicle_selection(self, selected_vehicle):
        """Update vehicle button appearance to show selection"""
        for btn_frame, icon_frame, vehicle_name in self.vehicle_buttons:
            if vehicle_name == selected_vehicle:
                btn_frame.configure(fg_color="#4CAF50")  # Green for selected
                icon_frame.configure(fg_color="#2E7D32")  # Darker green for icon
            else:
                btn_frame.configure(fg_color="#E8E8E8")  # Light gray for unselected
                icon_frame.configure(fg_color="#9C9C9C")  # Gray for icon
    
    def reset_vehicle_selection(self):
        """Reset all vehicle buttons to unselected state"""
        for btn_frame, icon_frame, _ in self.vehicle_buttons:
            btn_frame.configure(fg_color="#E8E8E8")
            icon_frame.configure(fg_color="#9C9C9C")
    
    def on_window_configure(self, event):
        """Handle window resize events with debouncing"""
        if event.widget == self.window:
            if self.resize_job_id:
                self.window.after_cancel(self.resize_job_id)
            self.resize_job_id = self.window.after(150, self.resize_components)
    
    def initial_resize(self):
        """Perform initial resize of components"""
        self.window.after(100, self.resize_components)
    
    def resize_components(self):
        """Resize and reposition components based on window size"""
        try:
            self.window.update_idletasks()
            # The new layout is responsive by design with CTk's pack manager
            pass
        except Exception as e:
            print(f"Error resizing components: {e}")
    def confirm_ride(self, selected_vehicle):
        """Update UI to reflect the ride confirmation and show the driver information"""
        
        # Update driver info based on the selected vehicle
        self.update_driver_info(selected_vehicle)

        # Disable vehicle selection (you can also hide the section or change its appearance)
        self.disable_vehicle_selection()

        # Change the "Confirm" button to "Ride Confirmed"
        self.update_confirmation_button()

        # Show confirmation message or status
        self.show_confirmation_message()

    def update_confirmation_button(self):
        """Update the 'Confirm' button to show a 'Ride Confirmed' status"""
        for button in self.action_buttons:
            if button.cget("text") == "Confirm":
                button.configure(text="Ride Confirmed", fg_color="#8BC34A", hover_color="#7B9F41")
                button.configure(state="disabled")

    def show_confirmation_message(self):
        """Display a confirmation message at the top of the UI after the ride is confirmed"""
        confirmation_message = ctk.CTkLabel(
            self.right_panel,
            text="Your ride has been confirmed! 🚗",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4CAF50"
        )
        confirmation_message.pack(fill="x", pady=(20, 15))

    def disable_vehicle_selection(self):
        """Disable the vehicle selection section after confirmation"""
        for btn_frame, _, vehicle_name in self.vehicle_buttons:
            btn_frame.configure(state="disabled")
        
        # Optionally, you could hide the vehicle selection panel after confirmation:
        self.left_panel.pack_forget()  # Hides the left panel after confirmation (e.g., map)
