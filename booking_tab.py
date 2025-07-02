import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "ManageVehicle_Page" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class BaseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application Base")
        self.geometry("1024x768")
        self.configure(fg_color="#FFFFFF")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Dictionary to store image references
        self.image_references = {}
        
        # Scaling factors
        self.scale_factor = 0.8  # Adjust this to scale the entire UI
        
        self.create_base_widgets()
        self.create_tab_frames()

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

    def create_base_widgets(self):
        """Create the base UI structure (header, sidebar, etc.)"""
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
        logo_img = self.load_and_resize_image("image_2.png", (398, 193))
        logo_label = ctk.CTkLabel(
            self.top_bar,
            image=logo_img,
            text="",
            fg_color="transparent"
        )
        logo_label.place(x=15, y=-1)

        # Main title label inside the top bar
        title_label = ctk.CTkLabel(
            self.top_bar,
            text="Just Book and Go.",
            text_color="#FFFFFF",
            font=("Jaro Regular", int(64 * self.scale_factor)),
            fg_color="#610C09"
        )
        title_label.place(x=300, y=45)

    def create_tab_frames(self):
        """Create the different tab content frames"""
        # Dashboard tab
        self.dashboard_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=0)
        label = ctk.CTkLabel(self.dashboard_frame, text="Dashboard Content", font=("Arial", 24))
        label.pack()

        # Manage Booking tab
        self.manage_booking_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=0)
        label = ctk.CTkLabel(self.manage_booking_frame, text="Manage Booking Content", font=("Arial", 24))
        label.pack()

        # Store the frames in a dictionary for easy access
        self.tab_frames = {
            "Dashboard": self.dashboard_frame,
            "Manage Booking": self.manage_booking_frame
        }

        # Initially hide all tabs (frames)
        self.hide_all_tabs()

        # Show the first tab by default
        self.show_dashboard_tab()

    # Tab switching methods
    def show_dashboard_tab(self):
        self.show_tab("Dashboard")

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

if __name__ == "__main__":
    app = BaseApp()
    app.resizable(False, False)
    app.mainloop()