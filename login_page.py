import customtkinter as ctk
from pathlib import Path
from PIL import Image
from user_data import load_users_from_csv
from tkinter import messagebox
import bcrypt
from admin import verify_admin  # Import your admin verification function
# ================ APPLICATION CONFIGURATION ================
# Set UI appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================ PATH MANAGEMENT ================
# Configure paths for asset files
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "Login_Page" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ================ AUTHENTICATION HELPERS ================
def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify password against stored bcrypt hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

# ================ MAIN LOGIN APPLICATION ================
class LoginApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("1440x1024")
        self.window.title("Just Book and Go")
        self.window.configure(fg_color="#610C09")
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(
            self.window,
            width=1440,
            height=1024,
            fg_color="#610C09",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True)
        main_frame.pack_propagate(False)

        # Logo
        logo_image = ctk.CTkImage(
            light_image=Image.open(relative_to_assets("image_1.png")),
            dark_image=Image.open(relative_to_assets("image_1.png")),
            size=(300, 200)
        )
        logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
        logo_label.place(x=512, y=5)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Just Book and Go.",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.place(x=522, y=190)

        # Username entry
        self.username_entry = ctk.CTkEntry(
            main_frame,
            width=614,
            height=55,
            placeholder_text="Enter your username",
            font=ctk.CTkFont(size=16),
            fg_color="#BFBFBF",
            text_color="#000716",
            placeholder_text_color="#666666",
            border_color="#BFBFBF",
            corner_radius=5
        )
        self.username_entry.place(x=401, y=300)

        ctk.CTkLabel(
            main_frame,
            text="Username:",
            font=ctk.CTkFont(size=24),
            text_color="#FFFFFF"
        ).place(x=379, y=250)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            main_frame,
            width=614,
            height=55,
            placeholder_text="Enter your password",
            show="*",
            font=ctk.CTkFont(size=16),
            fg_color="#BFBFBF",
            text_color="#000716",
            placeholder_text_color="#666666",
            border_color="#BFBFBF",
            corner_radius=5
        )
        self.password_entry.place(x=401, y=450)

        ctk.CTkLabel(
            main_frame,
            text="Password:",
            font=ctk.CTkFont(size=24),
            text_color="#FFFFFF"
        ).place(x=379, y=400)

        # Buttons
        ctk.CTkButton(
            main_frame,
            width=281,
            height=67,
            text="LOGIN",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#7A1511",
            hover_color="#8A1511",
            text_color="#FFFFFF",
            corner_radius=10,
            command=self.login_clicked
        ).place(x=568, y=530)

        ctk.CTkButton(
            main_frame,
            width=281,
            height=67,
            text="SIGN UP",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#7A1511",
            hover_color="#8A1511",
            text_color="#FFFFFF",
            corner_radius=10,
            command=self.open_signup
        ).place(x=568, y=630)

    def login_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check admin credentials first
        if verify_admin(username, password):
            messagebox.showinfo("Success", "Admin login successful!")
            self.open_admin_dashboard()
            return
        
        # Check regular user credentials
        users_db = load_users_from_csv()
        user = users_db.get(username)
        
        if user and verify_password(user.get_password(), password):
            messagebox.showinfo("Success", "Login successful!")
            self.open_user_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_admin_dashboard(self):
        """Open admin dashboard window"""
        self.window.destroy()
        from Admin_Dashboard  import ManageVehicleApp  # Changed from AdminDashboard
        admin_app = ManageVehicleApp()
        admin_app.mainloop()

    def open_user_dashboard(self):
        """Open regular user dashboard window"""
        self.window.destroy()
        from user_dashboard import UserDashboard
        user_app = UserDashboard()
        user_app.run()

    def open_signup(self):
        self.window.destroy()
        from signup import SignupApp
        signup_app = SignupApp(return_to_login=True)
        signup_app.run()

    def run(self):
        self.window.resizable(False, False)
        self.window.mainloop()

# ================ APPLICATION ENTRY POINT ================
if __name__ == "__main__":
    app = LoginApp()
    app.run()