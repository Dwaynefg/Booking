import customtkinter as ctk
from tkinter import StringVar, messagebox
from PIL import Image
from CALCULATIONS.fare_calculation import FareCalculator
import os

class RightPanel:
    """Manages the right panel components - vehicle selection, driver info, and payment"""
    
    def __init__(self, parent_frame, parent_app, driver_manager):
        self.parent_frame = parent_frame
        self.parent_app = parent_app
        self.driver_manager = driver_manager
        
        # Payment mode variable
        self.payment_mode = StringVar(value="Cash")
        
        # Selected vehicle tracking
        self.selected_vehicle = None
        self.selected_vehicle_price = "0 Pesos"

        # Fare calculator instance
        self.fare_calculator = FareCalculator()
        
        # Location coordinates (will be set from left panel)
        self.pickup_coordinates = None  # (lat, lng)
        self.dropoff_coordinates = None  # (lat, lng)

        # UI Components
        self.price_label = None
        self.price_breakdown_button = None
        self.vehicle_buttons = []
        self.action_buttons = []
        self.payment_radio_buttons = []
        
        # Driver info components
        self.driver_name_value = None
        self.plate_value = None
        self.vehicle_desc_value = None
        self.contact_value = None
        
        # Load vehicle icons
        self.vehicle_icons = self.load_vehicle_icons()
        
        self.setup_right_panel()

    def load_vehicle_icons(self):
        """Load and resize vehicle icons using CTkImage"""
        icons = {}
        icon_size = (24, 24)  # Slightly smaller to fit better in circles
    
        try:
            # Try multiple file extensions and paths
            icon_paths = {
                'car': [
                    'assets_copy/car.jpg', 
                    'assets_copy/car.jpeg',
                    'assets_copy/car.png',
                    'car.jpg',
                    'car.jpeg',
                    'car.png'
                ],
                'motorcycle': [
                    'assets_copy/motorcycle.jpg',
                    'assets_copy/motorcycle.jpeg',
                    'assets_copy/motorcycle.png',
                    'motorcycle.jpg',
                    'motorcycle.jpeg',
                    'motorcycle.png'
                ],
                'van': [
                    'assets_copy/van.jpg',
                    'assets_copy/van.jpeg',
                    'assets_copy/van.png',
                    'van.jpg',
                    'van.jpeg',
                    'van.png'
                ]
            }
        
            for vehicle_type, paths in icon_paths.items():
                icon_loaded = False
                for path in paths:
                    if os.path.exists(path):
                        try:
                            print(f"Trying to load {vehicle_type} icon from {path}")
                            # Load the image using PIL
                            pil_image = Image.open(path)
                            # Convert to RGBA if not already
                            if pil_image.mode != 'RGBA':
                                pil_image = pil_image.convert('RGBA')
                            # Create CTkImage which handles high DPI properly
                            icons[vehicle_type] = ctk.CTkImage(
                                light_image=pil_image,
                                dark_image=pil_image,
                                size=icon_size
                            )
                            print(f"Successfully loaded {vehicle_type} icon from {path}")
                            icon_loaded = True
                            break
                        except Exception as e:
                            print(f"Error loading {path}: {e}")
                            continue
                    else:
                        print(f"File not found: {path}")
            
                if not icon_loaded:
                    print(f"Could not find icon for {vehicle_type}, using emoji fallback")
                    icons[vehicle_type] = None  # We'll handle this in the UI creation
                    
        except Exception as e:
            print(f"Error loading vehicle icons: {e}")
            # Set all icons to None for emoji fallback
            for vehicle_type in ['car', 'motorcycle', 'van']:
                icons[vehicle_type] = None
    
        return icons
    
    def setup_right_panel(self):
        """Setup the right panel with vehicle selection, driver info, and payment"""
        # Vehicle selection section
        self.create_vehicle_selection()
        
        # Driver information section  
        self.create_driver_info()
        
        # Payment section
        self.create_payment_section()
        
        # Action buttons at the bottom
        self.create_action_buttons()
    
    def create_vehicle_selection(self):
        """Create vehicle selection section with clickable frames instead of buttons"""
        vehicle_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        vehicle_frame.pack(fill="x", pady=(0, 20))
    
        # Section title
        title_label = ctk.CTkLabel(vehicle_frame, text="Select Vehicle Type", font=ctk.CTkFont(size=16, weight="bold"), text_color="#000000")
        title_label.pack(anchor="w", pady=(0, 15))
    
        # Vehicle options with clickable frames
        vehicles = [
            ("Car(4 Seater)", "₱ 100.00", "car"),
            ("Car(6 Seater)", "₱ 120.00", "car"), 
            ("Mini Van", "₱ 200.00", "van"),
            ("Van", "₱ 250.00", "van"),
            ("Motorcycle", "₱ 50.00", "motorcycle")
        ]
    
        self.vehicle_buttons = []
        for i, (vehicle_name, price, icon_type) in enumerate(vehicles):
            # Create clickable frame instead of button
            vehicle_option_frame = ctk.CTkFrame(
                vehicle_frame,
                height=45,
                fg_color="#E8E8E8",
                corner_radius=5,
                cursor="hand2"
            )
            vehicle_option_frame.pack(fill="x", pady=2)
            vehicle_option_frame.pack_propagate(False)
        
            # Bind click event to the frame
            vehicle_option_frame.bind(
                "<Button-1>", 
                lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
            )
        
            # Create content frame inside clickable frame
            content_frame = ctk.CTkFrame(vehicle_option_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=15, pady=7)
        
            # Also bind click to content frame
            content_frame.bind(
                "<Button-1>", 
                lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
            )
        
            # Vehicle icon circle
            icon_frame = ctk.CTkFrame(content_frame, width=30, height=30, fg_color="#9C9C9C", corner_radius=15)
            icon_frame.pack(side="left", padx=(0, 10))
            icon_frame.pack_propagate(False)
        
            # Bind click to icon frame too
            icon_frame.bind(
                "<Button-1>", 
                lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
            )
        
            # Add icon to circle if available
            if self.vehicle_icons.get(icon_type):
                icon_label = ctk.CTkLabel(
                    icon_frame,
                    text="",
                    image=self.vehicle_icons[icon_type],
                    width=30,
                    height=30
                )
                icon_label.pack(expand=True)
                # Bind click to icon label
                icon_label.bind(
                    "<Button-1>", 
                    lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
                )
            else:
                # Fallback emoji icons
                emoji_map = {
                    "car": "🚗",
                    "van": "🚐",
                    "motorcycle": "🏍️"
                }
                emoji_label = ctk.CTkLabel(
                    icon_frame,
                    text=emoji_map.get(icon_type, "🚗"),
                    font=ctk.CTkFont(size=16)
                )
                emoji_label.pack(expand=True)
                # Bind click to emoji label
                emoji_label.bind(
                    "<Button-1>", 
                    lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
                )
        
            # Vehicle name
            name_label = ctk.CTkLabel(content_frame, text=vehicle_name, font=ctk.CTkFont(size=12, weight="bold"), text_color="#000000")
            name_label.pack(side="left")
            # Bind click to name label
            name_label.bind(
                "<Button-1>", 
                lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
            )
        
            # Price
            price_label = ctk.CTkLabel(content_frame, text=price, font=ctk.CTkFont(size=12, weight="bold"), text_color="#000000")
            price_label.pack(side="right")
            # Bind click to price label
            price_label.bind(
                "<Button-1>", 
                lambda e, vn=vehicle_name, p=price: self.select_vehicle(vn, p)
            )
        
            # Store frame reference
            self.vehicle_buttons.append(vehicle_option_frame)
    
    def select_vehicle(self, vehicle_name, price):
        """Handle vehicle selection"""
        self.selected_vehicle = vehicle_name
        
        # If we have coordinates, calculate the actual fare
        if self.pickup_coordinates and self.dropoff_coordinates:
            pickup_lat, pickup_lng = self.pickup_coordinates
            dropoff_lat, dropoff_lng = self.dropoff_coordinates
            
            fare_info = self.fare_calculator.calculate_fare(
                pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, vehicle_name
            )
            
            formatted_fare = self.fare_calculator.format_fare_display(fare_info)
            self.selected_vehicle_price = formatted_fare
            self.price_label.configure(text=formatted_fare.replace(".00", " Pesos"))
            
            # Store the current fare info
            self.current_fare_info = fare_info
        else:
            # Use the original price if no coordinates available
            self.selected_vehicle_price = price
            self.price_label.configure(text=price.replace(".00", " Pesos"))
        
        # Visual feedback - highlight selected frame
        for i, frame in enumerate(self.vehicle_buttons):
            if i == self.get_vehicle_index(vehicle_name):
                frame.configure(fg_color="#520000")
                self.update_frame_text_color(frame, "white")
            else:
                frame.configure(fg_color="#E8E8E8")
                self.update_frame_text_color(frame, "#000000")
        
        print(f"Selected vehicle: {vehicle_name} - {self.selected_vehicle_price}")
    
    def update_frame_text_color(self, frame, color):
        """Recursively update text color for all labels in a frame"""
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=color)
            elif isinstance(widget, ctk.CTkFrame):
                self.update_frame_text_color(widget, color)
    
    def get_vehicle_index(self, vehicle_name):
        """Get the index of a vehicle by name"""
        vehicles = ["Car(4 Seater)", "Car(6 Seater)", "Mini Van", "Van", "Motorcycle"]
        try:
            return vehicles.index(vehicle_name)
        except ValueError:
            return -1
    
    def create_driver_info(self):
        """Create driver information section"""
        self.driver_frame = ctk.CTkFrame(self.parent_frame, fg_color="#F5F5F5", border_width=1, border_color="#CCCCCC")
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
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Driver Name
        driver_name_label = ctk.CTkLabel(
            left_col,
            text="Driver Name:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#000000"
        )
        driver_name_label.pack(anchor="w")

        self.driver_name_value = ctk.CTkLabel(
            left_col,
            text="N/A",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#666666"
        )
        self.driver_name_value.pack(anchor="w", pady=(2, 8))

        # Plate Number
        plate_label = ctk.CTkLabel(
            left_col,
            text="Plate Number:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#000000"
        )
        plate_label.pack(anchor="w")

        self.plate_value = ctk.CTkLabel(
            left_col,
            text="N/A",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#666666"
        )
        self.plate_value.pack(anchor="w", pady=(2, 0))

        # Right column  
        right_col = ctk.CTkFrame(details_frame, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Vehicle Description
        vehicle_desc_label = ctk.CTkLabel(
            right_col,
            text="Vehicle Description:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#000000"
        )
        vehicle_desc_label.pack(anchor="w")

        self.vehicle_desc_value = ctk.CTkLabel(
            right_col,
            text="N/A",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#666666"
        )
        self.vehicle_desc_value.pack(anchor="w", pady=(2, 8))

        # Contact Number
        contact_label = ctk.CTkLabel(
            right_col,
            text="Contact Number:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#000000"
        )
        contact_label.pack(anchor="w")

        self.contact_value = ctk.CTkLabel(
            right_col,
            text="N/A",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#666666"
        )
        self.contact_value.pack(anchor="w", pady=(2, 0))

    def update_driver_info(self, driver_info):
        """Update driver information display with the provided driver details"""
        if driver_info:
            self.driver_name_value.configure(text=driver_info['driver_name'])
            self.plate_value.configure(text=driver_info['plate_no'])
            self.vehicle_desc_value.configure(text=driver_info['vehicle_name'])
            self.contact_value.configure(text=driver_info['contact_no'])
        else:
            # Reset to default if no driver info provided
            self.driver_name_value.configure(text="N/A")
            self.plate_value.configure(text="N/A")
            self.vehicle_desc_value.configure(text="N/A")
            self.contact_value.configure(text="N/A")

    def create_payment_section(self):
        """Create payment mode selection section"""
        payment_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        payment_frame.pack(fill="x", pady=(0, 20))
        
        # Price display with breakdown button
        price_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=(0, 15))
        
        # Price label and breakdown button on same row
        price_row_frame = ctk.CTkFrame(price_frame, fg_color="transparent")
        price_row_frame.pack(fill="x", pady=(0, 10))
        
        # Price section (left side)
        price_section_frame = ctk.CTkFrame(price_row_frame, fg_color="transparent")
        price_section_frame.pack(side="left", fill="x", expand=True)
        
        price_text_label = ctk.CTkLabel(
            price_section_frame,
            text="Price:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        )
        price_text_label.pack(side="left")
        
        self.price_label = ctk.CTkLabel(
            price_section_frame,
            text="0 Pesos",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#520000"
        )
        self.price_label.pack(side="left", padx=(10, 0))
        
        # Price breakdown button (right side)
        self.price_breakdown_button = ctk.CTkButton(
            price_row_frame,
            text="💰 Price Breakdown",
            width=150,
            height=30,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#520000",
            hover_color="#420000",
            corner_radius=15,
            command=self.show_price_breakdown
        )
        self.price_breakdown_button.pack(side="right", padx=(10, 0))
        
        # Payment mode selection
        payment_mode_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
        payment_mode_frame.pack(fill="x")
        
        mode_title = ctk.CTkLabel(
            payment_mode_frame,
            text="Select Mode of Payment:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        )
        mode_title.pack(anchor="w", pady=(0, 10))
        
        # Payment options (horizontal layout)
        payment_options_frame = ctk.CTkFrame(payment_mode_frame, fg_color="transparent")
        payment_options_frame.pack(fill="x")
        
        # Cash option (left side)
        cash_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Cash",
            variable=self.payment_mode,
            value="Cash",
            font=ctk.CTkFont(size=11),
            text_color="#000000"
        )
        cash_radio.pack(side="left", padx=(0, 20))
        
        # Online Payment option (right side)
        online_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Online Payment",
            variable=self.payment_mode,
            value="Online Payment", 
            font=ctk.CTkFont(size=11),
            text_color="#000000"
        )
        online_radio.pack(side="left")
        
        self.payment_radio_buttons = [cash_radio, online_radio]

    def show_price_breakdown(self):
        """Show detailed price breakdown in a popup dialog"""
        if not self.selected_vehicle:
            messagebox.showinfo("Price Breakdown", "Please select a vehicle first to see the price breakdown.")
            return
            
        if not self.pickup_coordinates or not self.dropoff_coordinates:
            messagebox.showinfo("Price Breakdown", "Please set pickup and dropoff locations to see the detailed price breakdown.")
            return
        
        # Get detailed fare breakdown
        fare_breakdown = self.get_fare_breakdown()
        
        # Create custom dialog
        try:
            dialog = ctk.CTkToplevel(self.parent_frame)
            dialog.title("💰 Price Breakdown")
            dialog.geometry("400x500")
            dialog.transient(self.parent_frame)
            dialog.grab_set()
            
            # Center the dialog
            dialog.geometry("+%d+%d" % (
                self.parent_frame.winfo_rootx() + 50,
                self.parent_frame.winfo_rooty() + 50
            ))
            
            # Main frame
            main_frame = ctk.CTkFrame(dialog, fg_color="#F5F5F5")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = ctk.CTkLabel(
                main_frame,
                text="💰 Fare Breakdown",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#520000"
            )
            title_label.pack(pady=(15, 20))
            
            # Vehicle info
            vehicle_info = ctk.CTkLabel(
                main_frame,
                text=f"🚗 Vehicle: {self.selected_vehicle}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#000000"
            )
            vehicle_info.pack(pady=(0, 15))
            
            # Breakdown text
            breakdown_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=10)
            breakdown_frame.pack(fill="both", expand=True, pady=(0, 20))
            
            breakdown_text = ctk.CTkTextbox(
                breakdown_frame,
                height=300,
                font=ctk.CTkFont(size=12),
                text_color="#000000",
                fg_color="#FFFFFF",
                wrap="word"
            )
            breakdown_text.pack(fill="both", expand=True, padx=15, pady=15)
            breakdown_text.insert("1.0", fare_breakdown)
            breakdown_text.configure(state="disabled")
            
            # Close button
            close_button = ctk.CTkButton(
                main_frame,
                text="✖️ Close",
                width=100,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#520000",
                hover_color="#420000",
                command=dialog.destroy
            )
            close_button.pack(pady=(0, 15))
            
        except Exception as e:
            print(f"Error creating price breakdown dialog: {e}")
            # Fallback to simple messagebox
            messagebox.showinfo("💰 Price Breakdown", fare_breakdown)

    def create_action_buttons(self):
        """Create Cancel and Confirm buttons"""
        buttons_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
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

    def set_location_coordinates(self, pickup_coords, dropoff_coords):
        """Set location coordinates for fare calculation"""
        self.pickup_coordinates = pickup_coords
        self.dropoff_coordinates = dropoff_coords
        
        # Update fare display if both coordinates are available
        if pickup_coords and dropoff_coords:
            self.update_all_vehicle_prices()
            if self.selected_vehicle:
                # Recalculate fare for selected vehicle
                self.select_vehicle(self.selected_vehicle, self.selected_vehicle_price)

    def update_all_vehicle_prices(self):
        """Update prices for all vehicles based on current route"""
        if not self.pickup_coordinates or not self.dropoff_coordinates:
            return
            
        pickup_lat, pickup_lng = self.pickup_coordinates
        dropoff_lat, dropoff_lng = self.dropoff_coordinates
        
        # Get fares for all vehicles
        all_fares = self.fare_calculator.get_fare_for_all_vehicles(
            pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
        )
        
        # Update vehicle button prices
        vehicle_names = ["Car(4 Seater)", "Car(6 Seater)", "Mini Van", "Van", "Motorcycle"]
        
        for i, vehicle_name in enumerate(vehicle_names):
            if i < len(self.vehicle_buttons):
                fare_info = all_fares.get(vehicle_name, {})
                formatted_price = self.fare_calculator.format_fare_display(fare_info)
                
                # Update the price label in the vehicle button frame
                self.update_vehicle_button_price(i, formatted_price)

    def update_vehicle_button_price(self, button_index, new_price):
        """Update the price display in a vehicle button"""
        if button_index >= len(self.vehicle_buttons):
            return
            
        vehicle_frame = self.vehicle_buttons[button_index]
        
        # Find and update the price label
        self.update_price_label_in_frame(vehicle_frame, new_price)

    def update_price_label_in_frame(self, frame, new_price):
        """Recursively find and update price label in frame"""
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                # Check if this label contains price text (starts with ₱)
                current_text = widget.cget("text")
                if current_text.startswith("₱"):
                    widget.configure(text=new_price)
                    return True
            elif isinstance(widget, ctk.CTkFrame):
                if self.update_price_label_in_frame(widget, new_price):
                    return True
        return False

    def reset_vehicle_selection(self):
        """Reset vehicle selection and prices"""
        self.selected_vehicle = None
        self.selected_vehicle_price = "0 Pesos"
        self.price_label.configure(text="0 Pesos")
    
        # Reset vehicle frame colors
        for frame in self.vehicle_buttons:
            frame.configure(fg_color="#E8E8E8")
            self.update_frame_text_color(frame, "#000000")
    
        # Reset vehicle prices to default
        self.reset_vehicle_prices_to_default()
    
        # Reset driver information
        self.update_driver_info(None)

    def reset_vehicle_prices_to_default(self):
        """Reset vehicle prices to default values"""
        default_prices = ["₱ 100.00", "₱ 120.00", "₱ 200.00", "₱ 250.00", "₱ 50.00"]
        
        for i, default_price in enumerate(default_prices):
            if i < len(self.vehicle_buttons):
                self.update_vehicle_button_price(i, default_price)

    def get_selected_vehicle(self):
        """Get currently selected vehicle"""
        return self.selected_vehicle
    
    def get_selected_vehicle_price(self):
        """Get currently selected vehicle price"""
        return self.selected_vehicle_price
    
    def get_payment_mode(self):
        """Get selected payment mode"""
        return self.payment_mode.get()
    
    def get_current_fare_info(self):
        """Get current fare information"""
        if hasattr(self, 'current_fare_info'):
            return self.current_fare_info
        return None

    def get_fare_breakdown(self):
        """Get detailed fare breakdown for display"""
        fare_info = self.get_current_fare_info()
        if fare_info:
            return self.fare_calculator.get_fare_breakdown_text(fare_info)
        return "No fare information available"