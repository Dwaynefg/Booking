import customtkinter as ctk
from tkinter import messagebox
from user import User
from user_data import load_users_from_csv, save_users_to_csv
from admin import verify_admin
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ride Booking System Login")
        self.geometry("400x350")

        # Load users from CSV on startup
        self.users_db = load_users_from_csv()

        self.frame_start = None
        self.frame_user_login = None
        self.frame_user_register = None
        self.frame_admin_login = None

        self.show_start_frame()

    def clear_frames(self):
        for frame in (self.frame_start, self.frame_user_login, self.frame_user_register, self.frame_admin_login):
            if frame:
                frame.destroy()

    def show_start_frame(self):
        self.clear_frames()
        self.frame_start = ctk.CTkFrame(self)
        self.frame_start.pack(pady=50, padx=50, fill="both", expand=True)

        label = ctk.CTkLabel(self.frame_start, text="Select Role", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        btn_user = ctk.CTkButton(self.frame_start, text="User", command=self.show_user_login_frame)
        btn_user.pack(pady=10)

        btn_admin = ctk.CTkButton(self.frame_start, text="Admin", command=self.show_admin_login_frame)
        btn_admin.pack(pady=10)

    def show_user_login_frame(self):
        self.clear_frames()
        self.frame_user_login = ctk.CTkFrame(self)
        self.frame_user_login.pack(pady=30, padx=30, fill="both", expand=True)

        label = ctk.CTkLabel(self.frame_user_login, text="User Login", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=10)

        email_label = ctk.CTkLabel(self.frame_user_login, text="Email:")
        email_label.pack()
        self.entry_email = ctk.CTkEntry(self.frame_user_login, width=250)
        self.entry_email.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_user_login, text="Login", command=self.user_login)
        btn_login.pack(pady=5)

        btn_register = ctk.CTkButton(self.frame_user_login, text="Create Account", command=self.show_user_register_frame)
        btn_register.pack(pady=5)

        btn_back = ctk.CTkButton(self.frame_user_login, text="Back", command=self.show_start_frame)
        btn_back.pack(pady=5)

    def user_login(self):
        email = self.entry_email.get().strip()
        if email in self.users_db:
            user = self.users_db[email]
            messagebox.showinfo("Login Success", f"Welcome back, {user.first_name or 'User'}!")
            #  Proceed to user dashboard
        else:
            messagebox.showerror("Login Failed", "User not found. Please register first.")

    def show_user_register_frame(self):
        self.clear_frames()
        self.frame_user_register = ctk.CTkFrame(self)
        self.frame_user_register.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(self.frame_user_register, text="Create User Account", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=10)

        self.reg_first_name = ctk.CTkEntry(self.frame_user_register, placeholder_text="First Name")
        self.reg_first_name.pack(pady=5)

        self.reg_last_name = ctk.CTkEntry(self.frame_user_register, placeholder_text="Last Name")
        self.reg_last_name.pack(pady=5)

        self.reg_email = ctk.CTkEntry(self.frame_user_register, placeholder_text="Email")
        self.reg_email.pack(pady=5)

        btn_create = ctk.CTkButton(self.frame_user_register, text="Create Account", command=self.create_user_account)
        btn_create.pack(pady=10)

        btn_back = ctk.CTkButton(self.frame_user_register, text="Back", command=self.show_user_login_frame)
        btn_back.pack(pady=5)

    def create_user_account(self):
        first = self.reg_first_name.get().strip()
        last = self.reg_last_name.get().strip()
        email = self.reg_email.get().strip()

        if not email:
            messagebox.showerror("Error", "Email is required.")
            return

        if email in self.users_db:
            messagebox.showerror("Error", "User already exists. Please login.")
            return

        new_user = User(email=email, first_name=first, last_name=last)
        self.users_db[email] = new_user

        save_users_to_csv(self.users_db)

        messagebox.showinfo("Success", f"Account created for {first}!")
        self.show_user_login_frame()

    def show_admin_login_frame(self):
        self.clear_frames()
        self.frame_admin_login = ctk.CTkFrame(self)
        self.frame_admin_login.pack(pady=50, padx=50, fill="both", expand=True)

        label = ctk.CTkLabel(self.frame_admin_login, text="Admin Login", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=10)

        self.admin_email_entry = ctk.CTkEntry(self.frame_admin_login, placeholder_text="Admin Email")
        self.admin_email_entry.pack(pady=5)

        self.admin_pass_entry = ctk.CTkEntry(self.frame_admin_login, placeholder_text="Password", show="*")
        self.admin_pass_entry.pack(pady=5)

        btn_login = ctk.CTkButton(self.frame_admin_login, text="Login", command=self.admin_login)
        btn_login.pack(pady=10)

        btn_back = ctk.CTkButton(self.frame_admin_login, text="Back", command=self.show_start_frame)
        btn_back.pack(pady=5)

    def admin_login(self):
        email = self.admin_email_entry.get().strip()
        password = self.admin_pass_entry.get().strip()

        if verify_admin(email, password):
            messagebox.showinfo("Admin Login", "Welcome Admin!")
            # TODO: proceed to admin dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
