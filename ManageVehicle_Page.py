import customtkinter as ctk
from vehicle import Vehicle  # Assuming your class code is in vehicles.py


class AdminVehicleEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin: Update Vehicle Cost per Km")
        self.geometry("500x300")

        self.vehicle_types = list(Vehicle.COST_PER_KM.keys())

        # Dropdown for vehicle type
        self.vehicle_label = ctk.CTkLabel(self, text="Select Vehicle Type:")
        self.vehicle_label.pack(pady=10)

        self.vehicle_dropdown = ctk.CTkOptionMenu(self, values=self.vehicle_types, command=self.on_vehicle_selected)
        self.vehicle_dropdown.pack()

        # Current cost label
        self.current_cost_label = ctk.CTkLabel(self, text="Current Cost per Km: -")
        self.current_cost_label.pack(pady=10)

        # Entry for new cost
        self.new_cost_entry = ctk.CTkEntry(self, placeholder_text="Enter new cost per km")
        self.new_cost_entry.pack(pady=10)

        # Save button
        self.save_button = ctk.CTkButton(self, text="Update Cost", command=self.update_cost)
        self.save_button.pack(pady=10)

        # Feedback label
        self.feedback_label = ctk.CTkLabel(self, text="", text_color="green")
        self.feedback_label.pack(pady=5)

    def on_vehicle_selected(self, vehicle_type):
        current_cost = Vehicle.COST_PER_KM.get(vehicle_type, "Unknown")
        self.current_cost_label.configure(text=f"Current Cost per Km: {current_cost}")
        self.feedback_label.configure(text="")

    def update_cost(self):
        vehicle_type = self.vehicle_dropdown.get()
        new_cost_str = self.new_cost_entry.get()

        try:
            new_cost = float(new_cost_str)
            if new_cost <= 0:
                raise ValueError("Cost must be positive.")

            Vehicle.COST_PER_KM[vehicle_type] = new_cost
            self.feedback_label.configure(text=f"Updated {vehicle_type} to {new_cost} per km!", text_color="green")
            self.on_vehicle_selected(vehicle_type)  # Refresh display
        except ValueError:
            self.feedback_label.configure(text="Invalid input. Enter a valid number.", text_color="red")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = AdminVehicleEditor()
    app.mainloop()
