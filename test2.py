import pandas as pd
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "ManageVehicle_Page" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
            height=15
        )
        self.scrollbar.config(command=self.tree.yview)
        
        # Load data
        self.load_data()
        
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            df = pd.read_csv(self.csv_file)
            
            if df.empty:
                df = pd.DataFrame(columns=[
                    "ID", "User", "Vehicle", "From", "To", 
                    "Distance", "Cost", "Status"
                ])
                df.to_csv(self.csv_file, index=False)
            
            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="w")
            
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))
                
            self.tree.pack(fill="both", expand=True)
                
        except FileNotFoundError:
            df = pd.DataFrame(columns=[
                "ID", "User", "Vehicle", "From", "To", 
                "Distance", "Cost", "Status"
            ])
            df.to_csv(self.csv_file, index=False)
            self.load_data()

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
            text="Driver Management",
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

class ManageVehicleTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.scale_factor = 0.8
        self.vehicle_entries = {}
        self.image_references = {}
        self.create_vehicle_cards_grid()
        
    def load_and_resize_image(self, image_path, size=None):
        if image_path not in self.image_references:
            img = Image.open(relative_to_assets(image_path))
            if size:
                scaled_size = (int(size[0] * self.scale_factor), 
                              int(size[1] * self.scale_factor))
                img = img.resize(scaled_size, Image.LANCZOS)
            self.image_references[image_path] = ImageTk.PhotoImage(img)
        return self.image_references[image_path]
        
    def create_vehicle_cards_grid(self):
        """Create an improved vehicle cards layout"""
        vehicle_cards = [
            {"type": "Motorcycle", "image": "image_3.png", "color": "#510000"},
            {"type": "6 Seater Car", "image": "image_5.png", "color": "#510000"},
            {"type": "4 Seater Car", "image": "image_4.png", "color": "#510000"},
            {"type": "Mini Van", "image": "image_7.png", "color": "#510000"},
            {"type": "Van", "image": "image_6.png", "color": "#510000"},
            {"type": "Add New", "image": "button_2.png", "color": "#FFBEBE", "is_add_button": True}
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
            command=self.add_vehicle_clicked
        ).place(relx=0.5, rely=0.4, anchor="center")

        ctk.CTkLabel(
            parent,
            text="Add New Vehicle",
            text_color="#000000",
            font=("Inter Medium", int(16 * self.scale_factor)),
        ).place(relx=0.5, rely=0.7, anchor="center")

    def create_save_button(self):
        """Create the save button at bottom right"""
        save_img = self.load_and_resize_image("button_1.png", (200, 30))
        save_button = ctk.CTkButton(
            self,
            image=save_img,
            text="",
            fg_color="transparent",
            hover_color="#E0E0E0",
            command=self.save_clicked
        )
        save_button.place(relx=0.9, rely=0.95, anchor="center")

    def add_vehicle_clicked(self):
        print("Add Vehicle button clicked - implement your logic here")

    def save_clicked(self):
        print("Save button clicked - implement your logic here")
        # Example of getting all entered prices:
        for vehicle_type, entry in self.vehicle_entries.items():
            print(f"{vehicle_type}: {entry.get()}")

class ManageVehicleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vehicle Management System")
        self.geometry("1024x768")
        self.configure(fg_color="#FFFFFF")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Dictionary to store image references
        self.image_references = {}
        self.scale_factor = 0.8
        
        # CSV files
        self.booking_csv = "ride_bookings.csv"
        self.driver_csv = "driver.csv"
        
        self.create_widgets()

    def load_and_resize_image(self, image_path, size=None):
        if image_path not in self.image_references:
            img = Image.open(relative_to_assets(image_path))
            if size:
                scaled_size = (int(size[0] * self.scale_factor), 
                              int(size[1] * self.scale_factor))
                img = img.resize(scaled_size, Image.LANCZOS)
            self.image_references[image_path] = ImageTk.PhotoImage(img)
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
        logo_img = self.load_and_resize_image("image_1.png", (48, 48))
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
            {"image": "button_3.png", "command": self.show_dashboard_tab},
            {"image": "button_5.png", "command": self.show_manage_vehicle_tab},
            {"image": "button_4.png", "command": self.show_manage_rider_tab}
        ]

        for button in nav_buttons:
            btn_img = self.load_and_resize_image(button["image"], (207, 53))
            btn = ctk.CTkButton(
                self.sidebar,
                image=btn_img,
                text="",
                fg_color="transparent",
                hover_color="#555555",
                command=button["command"]
            )
            btn.pack(fill="x", pady=5)

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
        ).place(x=15, y=-1)

        ctk.CTkLabel(
            self.top_bar,
            text="Just Book and Go.",
            text_color="#FFFFFF",
            font=("Jaro Regular", int(64 * self.scale_factor)),
            fg_color="#610C09"
        ).place(x=300, y=45)

        # Create tab frames
        self.create_tab_frames()

    def create_tab_frames(self):
        """Create the different tab content frames"""
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

    # Tab switching methods
    def show_dashboard_tab(self):
        self.hide_all_tabs()
        self.dashboard_frame.pack(fill="both", expand=True)

    def show_manage_vehicle_tab(self):
        self.hide_all_tabs()
        self.manage_vehicle_frame.pack(fill="both", expand=True)

    def show_manage_rider_tab(self):
        self.hide_all_tabs()
        self.manage_rider_frame.pack(fill="both", expand=True)

    def hide_all_tabs(self):
        for frame in self.tab_frames.values():
            frame.pack_forget()

if __name__ == "__main__":
    app = ManageVehicleApp()
    app.resizable(False, False)
    app.mainloop()