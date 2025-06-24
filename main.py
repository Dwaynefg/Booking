import tkinter as tk
from tkinter import ttk, messagebox
from booking_manager import BookingManager
from vehicle import Car, Van, Bike, CustomVehicle
from booking import Booking

class RideBookingApp:
    def __init__(self, master, current_user):
        self.master = master
        self.current_user = current_user
        self.master.title(f"Ride Booking System ({current_user.role})")
        self.manager = BookingManager()
        self.vehicles = {
            'Car': Car('Car', 1.0, 4),
            'Van': Van('Van', 1.5, 6),
            'Bike': Bike('Bike', 0.5, 2)
        }
        self.create_widgets()
        self.refresh_bookings()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding=10)
        frame.grid(row=0, column=0, sticky='ew')

        ttk.Label(frame, text="User:").grid(row=0, column=0)
        self.user_entry = ttk.Entry(frame)
        self.user_entry.grid(row=0, column=1)
        self.user_entry.insert(0, self.current_user.username)
        self.user_entry.config(state='readonly')

        ttk.Label(frame, text="Vehicle:").grid(row=1, column=0)
        self.vehicle_cb = ttk.Combobox(frame, values=list(self.vehicles.keys()))
        self.vehicle_cb.grid(row=1, column=1)

        ttk.Label(frame, text="Start:").grid(row=2, column=0)
        self.start_entry = ttk.Entry(frame)
        self.start_entry.grid(row=2, column=1)

        ttk.Label(frame, text="End:").grid(row=3, column=0)
        self.end_entry = ttk.Entry(frame)
        self.end_entry.grid(row=3, column=1)

        ttk.Label(frame, text="Distance (mi):").grid(row=4, column=0)
        self.distance_entry = ttk.Entry(frame)
        self.distance_entry.grid(row=4, column=1)

        ttk.Button(frame, text="Book Ride", command=self.book_ride).grid(row=5, column=0, columnspan=2, pady=5)

        if self.current_user.role == 'Admin':
            ttk.Button(frame, text="Add Vehicle Type", command=self.add_vehicle_popup).grid(row=6, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self.master, columns=('ID', 'User', 'Vehicle', 'Start', 'End', 'Distance', 'Cost'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self.master, text="Cancel Selected Booking", command=self.cancel_selected).grid(row=2, column=0, pady=5)

    def refresh_bookings(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in self.manager.bookings:
            self.tree.insert('', 'end', values=(b.booking_id, b.user, b.vehicle_type, b.start, b.end, b.distance, f"${b.cost:.2f}"))

    def book_ride(self):
        user = self.current_user.username
        vehicle_type = self.vehicle_cb.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        try:
            distance = float(self.distance_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Distance must be numeric.")
            return

        if not all([vehicle_type, start, end]):
            messagebox.showerror("Missing Info", "Please fill all fields.")
            return

        if vehicle_type not in self.vehicles:
            messagebox.showerror("Invalid Vehicle", "Vehicle type not recognized.")
            return

        vehicle = self.vehicles[vehicle_type]
        cost = vehicle.calculate_cost(distance)
        booking_id = len(self.manager.bookings) + 1
        booking = Booking(booking_id, user, vehicle_type, start, end, distance, cost)
        self.manager.add_booking(booking)
        self.refresh_bookings()
        messagebox.showinfo("Success", f"Ride booked. Cost: ${cost:.2f}")

    def cancel_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a booking to cancel.")
            return
        booking_id = self.tree.item(selected[0])['values'][0]
        self.manager.cancel_booking(booking_id, user=self.current_user.username, is_admin=self.current_user.role == 'Admin')
        self.refresh_bookings()

    def add_vehicle_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Add Vehicle Type")

        ttk.Label(popup, text="Name:").grid(row=0, column=0)
        name = ttk.Entry(popup); name.grid(row=0, column=1)

        ttk.Label(popup, text="Cost/Mile:").grid(row=1, column=0)
        cost = ttk.Entry(popup); cost.grid(row=1, column=1)

        ttk.Label(popup, text="Capacity:").grid(row=2, column=0)
        capacity = ttk.Entry(popup); capacity.grid(row=2, column=1)

        def add_vehicle():
            try:
                n = name.get()
                c = float(cost.get())
                cp = int(capacity.get())
                self.vehicles[n] = CustomVehicle(n, c, cp)
                self.vehicle_cb['values'] = list(self.vehicles.keys())
                popup.destroy()
                messagebox.showinfo("Vehicle Added", f"{n} added successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(popup, text="Add", command=add_vehicle).grid(row=3, column=0, columnspan=2)

def login_window():
    win = tk.Tk()
    win.title("Login")

    ttk.Label(win, text="Username:").grid(row=0, column=0)
    username_entry = ttk.Entry(win)
    username_entry.grid(row=0, column=1)

    ttk.Label(win, text="Role (User/Admin):").grid(row=1, column=0)
    role_entry = ttk.Entry(win)
    role_entry.grid(row=1, column=1)

    def on_login():
        username = username_entry.get().strip()
        role = role_entry.get().strip()
        if not username or not role:
            messagebox.showerror("Error", "Please enter username and role")
            return
        if role not in ('User', 'Admin'):
            messagebox.showerror("Error", "Role must be 'User' or 'Admin'")
            return
        win.destroy()
        root = tk.Tk()
        app = RideBookingApp(root, current_user=User(username, role))
        root.mainloop()

    ttk.Button(win, text="Login", command=on_login).grid(row=2, column=0, columnspan=2, pady=10)

    win.mainloop()

# Run the app
if __name__ == "__main__":
    login_window()
