import customtkinter as ctk
from pathlib import Path
from PIL import Image
from Modules.user_data import load_users_from_csv
from tkinter import messagebox
import bcrypt
from Modules.admin import verify_admin  # Import your admin verification function

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "Login_Page" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verify password against stored bcrypt hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

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
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open(relative_to_assets("image_1.png")),
                dark_image=Image.open(relative_to_assets("image_1.png")),
                size=(300, 200)
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.place(x=512, y=5)
        except Exception as e:
            print(f"Could not load logo image: {e}")
            # Create a text logo as fallback
            ctk.CTkLabel(
                main_frame,
                text="GO-DO",
                font=ctk.CTkFont(size=48, weight="bold"),
                text_color="#FFFFFF"
            ).place(x=650, y=80)

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

        # Bind Enter key to login
        self.window.bind('<Return>', lambda event: self.login_clicked())

    def login_clicked(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check admin credentials first
        if verify_admin(username, password):
            messagebox.showinfo("Success", f"Welcome Admin {username}!")
            self.open_admin_dashboard(username)
            return
        
        # Check regular user credentials
        try:
            users_db = load_users_from_csv()
            user = users_db.get(username)
            
            if user and verify_password(user.get_password(), password):
                messagebox.showinfo("Success", f"Welcome {username}!")
                self.launch_ride_booking_app(username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            print(f"Login error: {e}")
            messagebox.showerror("Error", "An error occurred during login. Please try again.")

    def launch_ride_booking_app(self, username):
        """Launch the main ride booking application (app2.py)"""
        try:
            self.window.destroy()
            
            # Import and launch the main ride booking app
            from Booking_page import MapWithDistanceRideBookingApp
            
            # Create and run the main application
            ride_app = MapWithDistanceRideBookingApp()
            
            # Store user information in the app if needed
            ride_app.current_user = username
            
            # Add logout functionality
            ride_app.setup_logout_callback(self.return_to_login)
            
            ride_app.run()
            
        except ImportError as e:
            messagebox.showerror("Error", f"Could not load ride booking app: {e}")
            self.return_to_login()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.return_to_login()

    def open_admin_dashboard(self, username=None):
        """Open admin dashboard window"""
        self.window.destroy()
        from Admin_Dashboard  import ManageVehicleApp  # Changed from AdminDashboard
        admin_app = ManageVehicleApp()
        admin_app.mainloop()

    def open_signup(self):
        """Open signup window"""
        try:
            self.window.destroy()
            from signup import SignupApp
            signup_app = SignupApp(return_to_login=True)
            signup_app.run()
        except ImportError:
            messagebox.showerror("Error", "Signup page not available")
            self.return_to_login()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open signup page: {e}")
            self.return_to_login()

    def return_to_login(self):
        """Return to login screen"""
        try:
            # Create new login window
            new_login = LoginApp()
            new_login.run()
        except Exception as e:
            print(f"Error returning to login: {e}")

    def run(self):
        self.window.resizable(False, False)
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.run()