import customtkinter as ctk
from pathlib import Path
from PIL import Image
import bcrypt
from Modules.user import User
from Modules.user_data import save_users_to_csv, load_users_from_csv
from tkinter import messagebox

# Initialize CTk settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "Signup_page" / "Signup_page"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def hash_password(password: str) -> str:
    """Hash password using bcrypt with salt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

class SignupApp:
    def __init__(self, return_to_login=False):
        self.window = ctk.CTk()
        self.window.geometry("1024x768")
        self.window.title("Sign Up")
        self.window.configure(fg_color="#610C09")
        self.return_to_login = return_to_login
        self.users_db = load_users_from_csv()
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(
            self.window,
            width=1024,
            height=768,
            fg_color="#610C09",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True)
        main_frame.pack_propagate(False)

        # Logo
        logo_image = ctk.CTkImage(
            light_image=Image.open(relative_to_assets("image_1.png")),
            dark_image=Image.open(relative_to_assets("image_1.png")),
            size=(300, 100)
        )
        logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
        logo_label.place(x=362, y=10)

        # Form fields
        self.username_entry = ctk.CTkEntry(
            main_frame,
            width=424,
            height=60,
            placeholder_text="Enter username",
            font=ctk.CTkFont(size=16),
            fg_color="#BEBDBD",
            text_color="#000716",
            placeholder_text_color="#666666",
            corner_radius=5
        )
        self.username_entry.place(x=300, y=159)

        ctk.CTkLabel(
            main_frame,
            text="Username:",
            font=ctk.CTkFont(size=24),
            text_color="#FFFFFF"
        ).place(x=278, y=118)

        self.firstname_entry = ctk.CTkEntry(
            main_frame,
            width=424,
            height=60,
            placeholder_text="Enter first name",
            font=ctk.CTkFont(size=16),
            fg_color="#BEBDBD",
            text_color="#000716",
            placeholder_text_color="#666666",
            corner_radius=5
        )
        self.firstname_entry.place(x=300, y=275)

        ctk.CTkLabel(
            main_frame,
            text="First Name:",
            font=ctk.CTkFont(size=24),
            text_color="#FFFFFF"
        ).place(x=278, y=234)

        self.lastname_entry = ctk.CTkEntry(
            main_frame,
            width=424,
            height=60,
            placeholder_text="Enter last name",
            font=ctk.CTkFont(size=16),
            fg_color="#BEBDBD",
            text_color="#000716",
            placeholder_text_color="#666666",
            corner_radius=5
        )
        self.lastname_entry.place(x=300, y=391)

        ctk.CTkLabel(
            main_frame,
            text="Last Name:",
            font=ctk.CTkFont(size=24),
            text_color="#FFFFFF"
        ).place(x=278, y=350)

        self.password_entry = ctk.CTkEntry(
            main_frame,
            width=424,
            height=60,
            placeholder_text="Enter password",
            show="*",
            font=ctk.CTkFont(size=16),
            fg_color="#BEBDBD",
            text_color="#000716",
            placeholder_text_color="#666666",
            corner_radius=5
        )
        self.password_entry.place(x=300, y=507)

        ctk.CTkLabel(
            main_frame,
            text="Password:",
            font=ctk.CTkFont(size=24),
            text_color="#FFFFFF"
        ).place(x=278, y=467)

        # Sign Up button
        signup_button = ctk.CTkButton(
            main_frame,
            width=200,
            height=50,
            text="SIGN UP",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#7A1511",
            hover_color="#8A1511",
            text_color="#FFFFFF",
            corner_radius=10,
            command=self.signup_clicked
        )
        signup_button.place(x=412, y=601)

    def signup_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.firstname_entry.get()
        last_name = self.lastname_entry.get()

        # Validation
        if not all([username, password]):
            messagebox.showerror("Error", "Username and password are required!")
            return

        if len(username) < 5:
            messagebox.showerror("Error", "Username must be at least 5 characters long!")
            return

        if username in self.users_db:
            messagebox.showerror("Error", "Username already exists!")
            return

        try:
            # Create new user with bcrypt hashed password
            hashed_password = hash_password(password)
            new_user = User(
                username=username,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name
            )

            # Add to database and save
            self.users_db[username] = new_user
            save_users_to_csv(self.users_db)
            messagebox.showinfo("Success", "Registration successful!")
            
            # Clear form
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.firstname_entry.delete(0, 'end')
            self.lastname_entry.delete(0, 'end')

            # Return to login if needed
            if self.return_to_login:
                self.window.destroy()
                from login_page import LoginApp
                login_app = LoginApp()
                login_app.run()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.window.resizable(False, False)
        self.window.mainloop()

if __name__ == "__main__":
    app = SignupApp()
    app.run()