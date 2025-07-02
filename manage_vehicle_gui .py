import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "ManageVehicle_Page" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ManageVehicleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Manage Vehicle")
        self.geometry("1024x768")  # Reduced window size
        self.configure(fg_color="#FFFFFF")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Dictionary to store image references
        self.image_references = {}
        
        # Scaling factors
        self.scale_factor = 0.8  # Adjust this to scale the entire UI
        
        self.create_widgets()

    def load_and_resize_image(self, image_path, size=None):
        """Load and resize an image while maintaining reference"""
        if image_path not in self.image_references:
            img = Image.open(relative_to_assets(image_path))
            if size:
                # Apply scaling factor to requested size
                scaled_size = (int(size[0] * self.scale_factor), 
                              int(size[1] * self.scale_factor))
                img = img.resize(scaled_size, Image.LANCZOS)
            self.image_references[image_path] = ImageTk.PhotoImage(img)
        return self.image_references[image_path]

    def scale_position(self, x, y):
        """Scale positions according to our scaling factor"""
        return (int(x * self.scale_factor), int(y * self.scale_factor))

    def create_widgets(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)

        # Top bar (scaled)
        top_bar_height = int(150 * self.scale_factor)
        self.top_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color="#610C09",  # Maroon color
            corner_radius=0,
            height=top_bar_height
        )
        self.top_bar.pack(fill="x", side="top")

        # Sidebar (scaled)
        sidebar_width = int(220 * self.scale_factor)
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            fg_color="#454545",
            corner_radius=0,
            width=sidebar_width
        )
        self.sidebar.pack(fill="y", side="left")

        # Sidebar logo and admin label
        logo_img = self.load_and_resize_image("image_1.png", (48, 48))
        logo_label = ctk.CTkLabel(
            self.sidebar,
            image=logo_img,
            text="",
            fg_color="transparent"
        )
        logo_label.pack(pady=int(70 * self.scale_factor))

        admin_label = ctk.CTkLabel(
            self.sidebar,
            text="ADMIN\n",
            text_color="#FFFFFF",
            font=("Inter", int(20 * self.scale_factor)),
            fg_color="transparent"
        )
        admin_label.pack()

        # Sidebar navigation buttons
        nav_buttons = [
            {"image": "button_3.png", "command": self.show_dashboard_tab},
            {"image": "button_5.png", "command": self.show_manage_vehicle_tab},
            {"image": "button_4.png", "command": self.show_manage_booking_tab}
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

        # Content frame (right side)
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True, side="right")

        # Main title and logo
        logo_img = self.load_and_resize_image("image_2.png", (398, 193))  # Resize it to fit within the top bar
        logo_label = ctk.CTkLabel(
            self.top_bar,
            image=logo_img,
            text="",
            fg_color="transparent"
        )
        logo_label.place(x=15, y=-1)   # Adds 10px padding from the top-left corner

        # Main title label inside the top bar
        title_label = ctk.CTkLabel(
            self.top_bar,  # Placing the title label in the top bar
            text="Just Book and Go.",
            text_color="#FFFFFF",
            font=("Jaro Regular", int(64 * self.scale_factor)),
            fg_color="#610C09"
        )
        title_label.place(x=300, y=45)

        # Create tab frames (content areas) but initially hide them
        self.create_tab_frames()

    def create_tab_frames(self):
        """Create the different tab content frames (dashboard, manage vehicle, etc.)"""

        # Dashboard tab
        self.dashboard_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=0)
        label = ctk.CTkLabel(self.dashboard_frame, text="Dashboard Content", font=("Arial", 24))
        label.pack()

        # Manage Vehicle tab (vehicle card grid)
        self.manage_vehicle_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=0)
        self.create_vehicle_cards_grid(self.manage_vehicle_frame)

        # Manage Booking tab
        self.manage_booking_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=0)
        label = ctk.CTkLabel(self.manage_booking_frame, text="Manage Booking Content", font=("Arial", 24))
        label.pack()

        # Store the frames in a dictionary for easy access
        self.tab_frames = {
            "Dashboard": self.dashboard_frame,
            "Manage Vehicle": self.manage_vehicle_frame,
            "Manage Booking": self.manage_booking_frame
        }

        # Initially hide all tabs (frames)
        self.hide_all_tabs()

        # Show the first tab (Manage Vehicle) by default
        self.show_manage_vehicle_tab()

    def create_vehicle_cards_grid(self, parent_frame):
        """Create vehicle cards layout in grid format"""

        vehicle_entries = {}
        vehicle_cards = [
            {"type": "Motorcycle", "image": "image_3.png"},
            {"type": "6 Seater Car", "image": "image_5.png"},
            {"type": "4 Seater Car", "image": "image_4.png"},
            {"type": "Mini Van", "image": "image_7.png"},
            {"type": "Van", "image": "image_6.png"},
            {"type": "Add New", "image": "button_2.png", "is_add_button": True}
        ]

        # Create a grid layout for vehicle cards
        for i, card in enumerate(vehicle_cards):
            row = i // 3
            col = i % 3

            # Card frame
            card_width = int(300 * self.scale_factor)
            card_height = int(280 * self.scale_factor)

            card_frame = ctk.CTkFrame(
                parent_frame,
                fg_color="#FFBEBE" if card.get("is_add_button") else "#510000",
                corner_radius=10,
                width=card_width,
                height=card_height
            )

            # Position cards in a grid
            pad_x = int(20 * self.scale_factor)
            pad_y = int(20 * self.scale_factor)
            start_x = int(50 * self.scale_factor)
            start_y = int(80 * self.scale_factor)

            x_pos = start_x + col * (card_width + pad_x)
            y_pos = start_y + row * (card_height + pad_y)

            card_frame.place(x=x_pos, y=y_pos)

            if card.get("is_add_button"):
                # Add Vehicle Card
                add_icon = self.load_and_resize_image(card["image"], (48, 48))
                ctk.CTkButton(
                    card_frame,
                    image=add_icon,
                    text="",
                    fg_color="transparent",
                    hover_color="#FFD0D0",
                    command=self.add_vehicle_clicked
                ).place(relx=0.5, rely=0.4, anchor="center")

                ctk.CTkLabel(
                    card_frame,
                    text="Add New Vehicle",
                    text_color="#000000",
                    font=("Inter Medium", int(16 * self.scale_factor)),
                ).place(relx=0.5, rely=0.7, anchor="center")
            else:
                # Regular Vehicle Card
                # Vehicle image
                vehicle_img = self.load_and_resize_image(card["image"], (150, 100))
                ctk.CTkLabel(
                    card_frame,
                    image=vehicle_img,
                    text="",
                    fg_color="transparent"
                ).place(relx=0.5, rely=0.3, anchor="center")

                # Vehicle type label
                ctk.CTkLabel(
                    card_frame,
                    text=card["type"],
                    text_color="#FFFFFF",
                    font=("Inter", int(18 * self.scale_factor)),
                ).place(relx=0.5, rely=0.55, anchor="center")

                # Cost per mile label
                ctk.CTkLabel(
                    card_frame,
                    text="Cost Per Mile",
                    text_color="#FFFFFF",
                    font=("Inter", int(16 * self.scale_factor)),
                ).place(relx=0.5, rely=0.65, anchor="center")

                # Peso sign and entry field
                entry_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
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
                vehicle_entries[card["type"]] = entry

        # Save Button (centered at bottom)
        save_img = self.load_and_resize_image("button_1.png", (200, 30))
        save_button = ctk.CTkButton(
            parent_frame,
            image=save_img,
            text="",
            fg_color="transparent",
            hover_color="#E0E0E0",
            command=self.save_clicked
        )
        save_button.place(relx=0.85, rely=0.95, anchor="center")

    # Tab switching methods
    def show_dashboard_tab(self):
        self.show_tab("Dashboard")

    def show_manage_vehicle_tab(self):
        self.show_tab("Manage Vehicle")

    def show_manage_booking_tab(self):
        self.show_tab("Manage Booking")

    def show_tab(self, tab_name):
        """Show the selected tab and hide others"""
        self.hide_all_tabs()
        self.tab_frames[tab_name].pack(fill="both", expand=True)

    def hide_all_tabs(self):
        """Hide all tab frames"""
        for frame in self.tab_frames.values():
            frame.pack_forget()

    # Button command methods
    def add_vehicle_clicked(self):
        print("Add Vehicle button clicked")

    def save_clicked(self):
        print("Save button clicked")

if __name__ == "__main__":
    app = ManageVehicleApp()
    app.resizable(False, False)
    app.mainloop()
