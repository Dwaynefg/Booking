import pandas as pd
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from pathlib import Path

# ====================== PATH CONFIGURATION ======================
# Set up paths for assets and data files
OUTPUT_PATH = Path(__file__).parent  # Root directory of the project
ASSETS_PATH = OUTPUT_PATH / "ManageVehicle_Page" / "frame0"  # UI assets
DATA_PATH = OUTPUT_PATH / "data"  # Where CSV files are stored

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ====================== BOOKING TABLE VIEW ======================
class BookingTableView(ctk.CTkFrame):
    def __init__(self, parent, csv_file):
        super().__init__(parent, fg_color="#FFFFFF")
        self.csv_file = csv_file
        
        # Create container frame
        self.container = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Booking Dashboard",
            text_color="#000000",
            font=("Inter", 24),
            fg_color="#FFFFFF"
        )
        self.title_label.pack(anchor="w", pady=(0, 20))
        
        # Create treeview with scrollbar
        self.tree_frame = ctk.CTkFrame(self.container, fg_color="#FFFFFF")
        self.tree_frame.pack(fill="both", expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.scrollbar.set,
            height=15,
            selectmode="extended",
            columns=("Driver_name", "Vehicle", "Pickup_point", 
                    "Destination", "Booking_ID", "Price", "Status"),
            show="headings"
        )
        self.scrollbar.config(command=self.tree.yview)
    
        # Configure column headings and properties
        columns_config = {
            "Driver_name": {"width": 120, "anchor": "w", "heading_anchor": "w"},
            "Vehicle": {"width": 100, "anchor": "center", "heading_anchor": "center"},
            "Pickup_point": {"width": 100, "anchor": "center", "heading_anchor": "center"},
            "Destination": {"width": 120, "anchor": "center", "heading_anchor": "center"},
            "Booking_ID": {"width": 100, "anchor": "center", "heading_anchor": "center"},
            "Price": {"width": 80, "anchor": "center", "heading_anchor": "center"},
            "Status": {"width": 80, "anchor": "center", "heading_anchor": "center"}
        }

        # Apply column configurations
        for col, config in columns_config.items():
            self.tree.heading(col, text=col, anchor=config["heading_anchor"])
            self.tree.column(col, width=config["width"], anchor=config["anchor"])
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                           rowheight=25,
                           font=('Inter', 12))
        self.style.configure("Treeview.Heading", 
                           font=('Inter', 12, 'bold'))
        
        # Load data
        self.load_data()
        
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            df = pd.read_csv(self.csv_file)
            
            if df.empty:
                df = pd.DataFrame(columns=[
                    "Driver_name", "Vehicle", "Pickup_point",
                "Destination","Booking_ID", "Price", "Status"
                ])
                df.to_csv(self.csv_file, index=False)
            
            # Filter and format the data
            display_columns = [
                "Driver_name", "Vehicle", "Pickup_point",
                "Destination","Booking_ID", "Price", "Status"
            ]
            
            # Format Price with currency symbol - FIXED VERSION
            if 'Price' in df.columns:
                def format_price(x):
                    if pd.isnull(x) or x == "":
                        return ""
                    try:
                        # If x is already a string, try to extract numeric value
                        if isinstance(x, str):
                            # Remove currency symbols and commas
                            clean_value = x.replace('₱', '').replace(',', '').strip()
                            if clean_value == "":
                                return ""
                            # Convert to float
                            numeric_value = float(clean_value)
                        else:
                            # If x is already numeric
                            numeric_value = float(x)
                        
                        # Format with currency symbol
                        return f"₱{numeric_value:,.2f}"
                    except (ValueError, TypeError):
                        # If conversion fails, return original value or empty string
                        return str(x) if x is not None else ""
                
                df['Price'] = df['Price'].apply(format_price)
            
            # Insert data with alternating row colors
            for i, row in df.iterrows():
                values = [row[col] if pd.notnull(row[col]) else "" for col in display_columns]
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=values, tags=(tag,))
            
            # Configure row colors
            self.tree.tag_configure('evenrow', background='#FFFFFF')
            self.tree.tag_configure('oddrow', background='#F5F5F5')
            
            self.tree.pack(fill="both", expand=True)
                
        except FileNotFoundError:
            df = pd.DataFrame(columns=[
                "Driver_name", "Vehicle", "Pickup_point",
                "Destination","Booking_ID", "Price", "Status"
            ])
            df.to_csv(self.csv_file, index=False)
            self.load_data()

# ====================== DRIVER TABLE VIEW ====================== 
class DriverTableView(ctk.CTkFrame):
    def __init__(self, parent, csv_file):
        super().__init__(parent, fg_color="#FFFFFF")
        self.csv_file = csv_file
        
        # Create container frame
        self.container = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Rider Directory",
            text_color="#000000",
            font=("Inter", 24),
            fg_color="#FFFFFF"
        )
        self.title_label.pack(anchor="w", pady=(0, 20))
        
        # Create treeview with scrollbar
        self.tree_frame = ctk.CTkFrame(self.container, fg_color="#FFFFFF")
        self.tree_frame.pack(fill="both", expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.scrollbar.set,
            height=15,
            selectmode="browse"
        )
        self.scrollbar.config(command=self.tree.yview)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                           rowheight=25,
                           font=('Inter', 12))
        self.style.configure("Treeview.Heading", 
                           font=('Inter', 12, 'bold'))
        
        # Load data
        self.load_data()
        
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Read from CSV
            df = pd.read_csv(self.csv_file)
            
            # Configure columns
            self.tree["columns"] = list(df.columns)
            self.tree.column("#0", width=0, stretch=False)  # Remove empty space
            
            # Set column headings and alignment
            for col in df.columns:
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, anchor="center", width=150)
            
            # Insert data
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))
                
            self.tree.pack(fill="both", expand=True)
        except FileNotFoundError:
            # Create empty CSV if it doesn't exist
            df = pd.DataFrame(columns=["Name", "Email", "Phone", "Vehicle", "Status"])
            df.to_csv(self.csv_file, index=False)
            self.load_data()

# ====================== VEHICLE MANAGEMENT TAB ======================
class ManageVehicleTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.scale_factor = 0.8
        self.vehicle_entries = {}
        self.image_references = {}
        self.create_vehicle_cards_grid()
        
    def load_and_resize_image(self, image_path, size=None):
        """Load image using CTkImage for proper scaling"""
        if image_path not in self.image_references:
            try:
                img = Image.open(relative_to_assets(image_path))
                if size:
                    scaled_size = (int(size[0] * self.scale_factor), 
                                  int(size[1] * self.scale_factor))
                    # Use CTkImage instead of ImageTk.PhotoImage
                    self.image_references[image_path] = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=scaled_size
                    )
                else:
                    self.image_references[image_path] = ctk.CTkImage(
                        light_image=img,
                        dark_image=img
                    )
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                # Return a placeholder CTkImage if loading fails
                placeholder = Image.new('RGB', (100, 100), color='gray')
                self.image_references[image_path] = ctk.CTkImage(
                    light_image=placeholder,
                    dark_image=placeholder,
                    size=(100, 100)
                )
        return self.image_references[image_path]
        
    def create_vehicle_cards_grid(self):
        """Create an improved vehicle cards layout"""
        vehicle_cards = [
            {"type": "Motorcycle", "image": "image_3.png", "color": "#510000"},
            {"type": "6 Seater Car", "image": "image_5.png", "color": "#510000"},
            {"type": "4 Seater Car", "image": "image_4.png", "color": "#510000"},
            {"type": "Mini Van", "image": "image_7.png", "color": "#510000"},
            {"type": "Van", "image": "image_6.png", "color": "#510000"},
        ]

        # Create a grid layout frame
        grid_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        grid_frame.pack(pady=(40, 20))

        # Create cards in a 2x3 grid
        for i, card in enumerate(vehicle_cards):
            row = i // 3
            col = i % 3

            card_frame = ctk.CTkFrame(
                grid_frame,
                fg_color=card["color"],
                corner_radius=10,
                width=int(300 * self.scale_factor),
                height=int(280 * self.scale_factor)
            )
            card_frame.grid(row=row, column=col, padx=15, pady=15)

            if card.get("is_add_button"):
                self.create_add_button_card(card_frame, card)
            else:
                self.create_vehicle_card(card_frame, card)

        # Save button at bottom right
        self.create_save_button()

    def create_vehicle_card(self, parent, card):
        """Create a standard vehicle card"""
        # Vehicle image
        vehicle_img = self.load_and_resize_image(card["image"], (150, 100))
        ctk.CTkLabel(
            parent,
            image=vehicle_img,
            text="",
            fg_color="transparent"
        ).place(relx=0.5, rely=0.3, anchor="center")

        # Vehicle type label
        ctk.CTkLabel(
            parent,
            text=card["type"],
            text_color="#FFFFFF",
            font=("Inter", int(18 * self.scale_factor)),
        ).place(relx=0.5, rely=0.55, anchor="center")

        # Cost per mile label
        ctk.CTkLabel(
            parent,
            text="Cost Per Mile",
            text_color="#FFFFFF",
            font=("Inter", int(16 * self.scale_factor)),
        ).place(relx=0.5, rely=0.65, anchor="center")

        # Price entry field
        entry_frame = ctk.CTkFrame(parent, fg_color="transparent")
        entry_frame.place(relx=0.5, rely=0.8, anchor="center")

        ctk.CTkLabel(
            entry_frame,
            text="₱",
            text_color="#FFFFFF",
            font=("Inter", int(20 * self.scale_factor)),
        ).pack(side="left", padx=5)

        entry = ctk.CTkEntry(
            entry_frame,
            width=int(120 * self.scale_factor),
            height=int(28 * self.scale_factor),
            fg_color="#747474",
            text_color="#000716",
            border_width=0,
            corner_radius=5
        )
        entry.pack(side="left")
        self.vehicle_entries[card["type"]] = entry

    def create_add_button_card(self, parent, card):
        """Create the 'Add New' button card"""
        add_icon = self.load_and_resize_image(card["image"], (48, 48))
        ctk.CTkButton(
            parent,
            image=add_icon,
            text="",
            fg_color="transparent",
            hover_color="#FFD0D0",
        ).place(relx=0.5, rely=0.4, anchor="center")

        ctk.CTkLabel(
            parent,
            text="Add New Vehicle",
            text_color="#000000",
            font=("Inter Medium", int(16 * self.scale_factor)),
        ).place(relx=0.5, rely=0.7, anchor="center")

    def create_save_button(self):
        """Create the save button at bottom right"""
        save_img = self.load_and_resize_image("button_1.png", (250, 50))
        save_button = ctk.CTkButton(
            self,
            image=save_img,
            text="",
            fg_color="transparent",
            hover_color="#E0E0E0",
            command=self.save_clicked
        )
        save_button.place(relx=0.9, rely=0.95, anchor="center")

    def save_clicked(self):
        """Handle save button click with confirmation and validation"""
        # Check if any entry has a value
        has_values = any(entry.get().strip() for entry in self.vehicle_entries.values())
        
        if not has_values:
            self.show_message("No Values Entered", "Please enter cost values before saving.")
            return
            
        # Ask for confirmation
        confirmed = self.ask_confirmation("Confirm Save", 
                                        "Are you sure you want to update the cost per mile?")
        
        if confirmed:
            # Process the save operation
            self.process_save()
            self.show_message("Success", "Cost per mile updated successfully!")
    
    def ask_confirmation(self, title, message):
        """Show a confirmation dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self)  # Set to be on top of main window
        dialog.grab_set()  # Modal dialog
        
        # Center the dialog
        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 200
            y = self.winfo_y() + (self.winfo_height() // 2) - 100
            dialog.geometry(f"+{x}+{y}")
        except:
            pass  # Fallback to default position
        
        # Message label
        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Inter", 14)
        ).pack(pady=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        result = {'confirmed': False}
        
        def on_confirm():
            result['confirmed'] = True
            dialog.destroy()
            
        def on_cancel():
            dialog.destroy()
        
        # Confirm button
        ctk.CTkButton(
            button_frame,
            text="Yes",
            command=on_confirm,
            width=100
        ).pack(side="left", padx=10)
        
        # Cancel button
        ctk.CTkButton(
            button_frame,
            text="No",
            command=on_cancel,
            width=100
        ).pack(side="left", padx=10)
        
        self.wait_window(dialog)
        return result['confirmed']
    
    def show_message(self, title, message):
        """Show an information message"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        try:
            x = self.winfo_x() + (self.winfo_width() // 2) - 200
            y = self.winfo_y() + (self.winfo_height() // 2) - 75
            dialog.geometry(f"+{x}+{y}")
        except:
            pass  # Fallback to default position
        
        # Message label
        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Inter", 14)
        ).pack(pady=20)
        
        # OK button
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack(pady=10)
        
        self.wait_window(dialog)
    
    def process_save(self):
        """Process the save operation (to be implemented)"""
        # Here you would save the values to your database or file
        for vehicle_type, entry in self.vehicle_entries.items():
            value = entry.get().strip()
            if value:
                print(f"Saving {vehicle_type}: {value}")
                # Add your save logic here

# ====================== MAIN APPLICATION ======================
class ManageVehicleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1024x768")
        self.configure(fg_color="#FFFFFF")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Dictionary to store image references
        self.image_references = {}
        self.scale_factor = 0.8
        
        # CSV files
        self.booking_csv = "book_history.csv"
        self.driver_csv = "data/driver.csv"
        
        # Navigation button tracking
        self.button_widgets = {}
        self.active_button = None
        self.content_frame = None
        
        # Initialize after a short delay to avoid Tkinter scheduling issues
        self.after(100, self.create_widgets)

    def load_and_resize_image(self, image_path, size=None):
        """Load image using CTkImage for proper scaling"""
        if image_path not in self.image_references:
            try:
                img = Image.open(relative_to_assets(image_path))
                if size:
                    scaled_size = (int(size[0] * self.scale_factor), 
                                  int(size[1] * self.scale_factor))
                    # Use CTkImage instead of ImageTk.PhotoImage
                    self.image_references[image_path] = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=scaled_size
                    )
                else:
                    self.image_references[image_path] = ctk.CTkImage(
                        light_image=img,
                        dark_image=img
                    )
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                # Return a placeholder CTkImage if loading fails
                placeholder = Image.new('RGB', (100, 100), color='gray')
                self.image_references[image_path] = ctk.CTkImage(
                    light_image=placeholder,
                    dark_image=placeholder,
                    size=(100, 100)
                )
        return self.image_references[image_path]

    def create_widgets(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Top bar
        self.top_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color="#610C09",
            corner_radius=0,
            height=int(150 * self.scale_factor)
        )
        self.top_bar.pack(fill="x", side="top")

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            fg_color="#454545",
            corner_radius=0,
            width=int(220 * self.scale_factor)
        )
        self.sidebar.pack(fill="y", side="left")

        # Sidebar logo and admin label
        logo_img = self.load_and_resize_image("image_1.png", (120, 120))
        ctk.CTkLabel(
            self.sidebar,
            image=logo_img,
            text="",
            fg_color="transparent"
        ).pack(pady=int(70 * self.scale_factor))

        ctk.CTkLabel(
            self.sidebar,
            text="ADMIN\n",
            text_color="#FFFFFF",
            font=("Inter", int(20 * self.scale_factor)),
            fg_color="transparent"
        ).pack()

        # Sidebar navigation buttons
        nav_buttons = [
            {"name": "dashboard", "image": "button_3.png", "active_image": "button_3_active.png", "command": self.show_dashboard_tab},
            {"name": "vehicle", "image": "button_5.png", "active_image": "button_5_active.png", "command": self.show_manage_vehicle_tab},
            {"name": "rider", "image": "button_4.png", "active_image": "button_4_active.png", "command": self.show_manage_rider_tab}
        ]

        for button in nav_buttons:
            # Load both normal and active images
            img_normal = self.load_and_resize_image(button["image"], (207, 53))
            img_active = self.load_and_resize_image(button["active_image"], (207, 53))
            
            btn = ctk.CTkButton(
                self.sidebar,
                image=img_normal if button["name"] != "dashboard" else img_active,
                text="",
                fg_color="transparent",
                hover_color="#555555",
                command=lambda b=button: self.handle_nav_button_click(b)
            )
            btn.pack(fill="x", pady=5)
            
            # Store button reference
            self.button_widgets[button["name"]] = btn
            
            # Set first button as active by default
            if button["name"] == "dashboard":
                self.active_button = button["name"]

        # Content frame
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True, side="right")

        # Main title and logo
        logo_img = self.load_and_resize_image("image_2.png", (398, 193))
        ctk.CTkLabel(
            self.top_bar,
            image=logo_img,
            text="",
            fg_color="transparent"
        ).place(x=0, y=-5)

        ctk.CTkLabel(
            self.top_bar,
            text="Just Book and Go.",
            text_color="#FFFFFF",
            font=("Jaro Regular", int(64 * self.scale_factor)),
            fg_color="#610C09"
        ).place(x=250, y=45)

        # Create tab frames after a short delay
        self.after(50, self.create_tab_frames)

    def handle_nav_button_click(self, button):
        """Handle navigation button clicks and image switching"""
        # Skip if clicking the already active button
        if self.active_button == button["name"]:
            return
            
        # Execute the button's command
        button["command"]()
        
        # Update button images
        self.set_active_button(button["name"])

    def set_active_button(self, button_name):
        """Set the active button state and update images"""
        # Set all buttons to normal state first
        for name, btn in self.button_widgets.items():
            normal_img = self.load_and_resize_image(f"button_{'3' if name == 'dashboard' else '5' if name == 'vehicle' else '4'}.png", (207, 53))
            btn.configure(image=normal_img)
        
        # Set the new active button
        if button_name:
            active_img = self.load_and_resize_image(f"button_{'3' if button_name == 'dashboard' else '5' if button_name == 'vehicle' else '4'}_active.png", (207, 53))
            self.button_widgets[button_name].configure(image=active_img)
            self.active_button = button_name

    def create_tab_frames(self):
        """Create the different tab content frames"""
        try:
            # Dashboard tab - Contains booking table
            self.dashboard_frame = BookingTableView(self.content_frame, self.booking_csv)

            # Manage Vehicle tab
            self.manage_vehicle_frame = ManageVehicleTab(self.content_frame)

            # Manage Rider tab - Contains driver table
            self.manage_rider_frame = DriverTableView(self.content_frame, self.driver_csv)

            # Store frames
            self.tab_frames = {
                "Dashboard": self.dashboard_frame,
                "Manage Vehicle": self.manage_vehicle_frame,
                "Manage Rider": self.manage_rider_frame
            }

            # Show Dashboard tab by default
            self.show_dashboard_tab()
        except Exception as e:
            print(f"Error creating tab frames: {e}")

    def show_dashboard_tab(self):
        if hasattr(self, 'tab_frames'):
            self.hide_all_tabs()
            self.dashboard_frame.pack(fill="both", expand=True)

    def show_manage_vehicle_tab(self):
        if hasattr(self, 'tab_frames'):
            self.hide_all_tabs()
            self.manage_vehicle_frame.pack(fill="both", expand=True)

    def show_manage_rider_tab(self):
        if hasattr(self, 'tab_frames'):
            self.hide_all_tabs()
            self.manage_rider_frame.pack(fill="both", expand=True)

    def hide_all_tabs(self):
        if hasattr(self, 'tab_frames'):
            for frame in self.tab_frames.values():
                frame.pack_forget()
                
    def run(self):
        self.resizable(False, False)
        self.mainloop()

# ====================== APPLICATION ENTRY POINT ======================
if __name__ == "__main__":
    app = ManageVehicleApp()
    app.run()