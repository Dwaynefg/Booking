import customtkinter as ctk
from vehicle import Car4Seater, Minivan, Bike
from booking import Booking
import booking_history as booking_logs
from datetime import datetime

# Load existing bookings
bookings = booking_logs.load_bookings_from_csv()

# Vehicle class options with default cost per mile
vehicle_options = {
    "Car4Seater": (Car4Seater, 1.5),
    "Minivan": (Minivan, 1.8),
    "Bike": (Bike, 0.9)
}

class BookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ride Booking System")
        self.geometry("800x600")

        # User input form
        self.create_form()

        # Booking list display
        self.booking_list = ctk.CTkTextbox(self, width=700, height=200)
        self.booking_list.grid(row=10, column=0, columnspan=2, padx=10, pady=20)
        self.refresh_booking_list()

    def create_form(self):
        labels = [
            "User Name", "Driver Name", "Pickup Location",
            "Drop-off Location", "Distance (km)",
            "Duration (min)", "Payment Method"
        ]
        self.entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(self, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self, width=300)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

        ctk.CTkLabel(self, text="Vehicle Type").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.vehicle_type_var = ctk.StringVar(value="Car4Seater")
        self.vehicle_dropdown = ctk.CTkOptionMenu(self, variable=self.vehicle_type_var, values=list(vehicle_options.keys()))
        self.vehicle_dropdown.grid(row=7, column=1, padx=10, pady=5)

        self.add_btn = ctk.CTkButton(self, text="Add Booking", command=self.add_booking)
        self.add_btn.grid(row=8, column=0, columnspan=2, pady=20)

    def add_booking(self):
        try:
            user = self.entries["User Name"].get().strip()
            driver = self.entries["Driver Name"].get().strip()
            pickup = self.entries["Pickup Location"].get().strip()
            dropoff = self.entries["Drop-off Location"].get().strip()
            distance = float(self.entries["Distance (km)"].get().strip())
            duration = int(self.entries["Duration (min)"].get().strip())
            payment = self.entries["Payment Method"].get().strip()
            vehicle_type = self.vehicle_type_var.get()

            if not all([user, driver, pickup, dropoff, payment]):
                self.show_message("Please fill in all fields.")
                return

            vehicle_class, cost_per_mile = vehicle_options[vehicle_type]
            vehicle = vehicle_class(name=f"{vehicle_type} Model", cost_per_mile=cost_per_mile)

            booking_id = str(int(datetime.now().timestamp()))

            booking = Booking(
                booking_id=booking_id,      # use snake_case here
                userName=user,
                driverName=driver,
                vehicle=vehicle,
                pickup=pickup,
                drop_off=dropoff,
                distance_km=distance,
                duration_min=duration,
                paymentMethod=payment,
                status="Pending"
            )

            bookings.append(booking)
            booking_logs.save_bookings_to_csv(bookings)
            self.refresh_booking_list()
            self.clear_form()
            self.show_message("Booking added successfully!")

        except ValueError:
            self.show_message("Please enter valid numbers for distance and duration.")

    def refresh_booking_list(self):
        self.booking_list.delete("1.0", "end")
        for b in bookings:
            self.booking_list.insert("end", str(b) + "\n\n")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def show_message(self, msg):
        from tkinter import messagebox
        messagebox.showinfo("Info", msg)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = BookingApp()
    app.mainloop()
    
