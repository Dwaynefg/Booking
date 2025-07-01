import tkinter as tk
from tkinter import ttk
 # Assuming this function loads all booking
class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("View All Bookings")
        
        # Create a frame for the treeview (table)
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a Treeview widget (table) to display bookings
        self.tree = ttk.Treeview(self.frame, columns=("Booking ID", "User", "Vehicle Type", "Start Location", "End Location", "Distance", "Total Cost"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define the column headings
        self.tree.heading("Booking ID", text="Booking ID")
        self.tree.heading("User", text="User")
        self.tree.heading("Vehicle Type", text="Vehicle Type")
        self.tree.heading("Start Location", text="Start Location")
        self.tree.heading("End Location", text="End Location")
        self.tree.heading("Distance", text="Distance (km)")
        self.tree.heading("Total Cost", text="Total Cost ($)")

        # Load and display the bookings in the Treeview
        self.display_bookings()

    def display_bookings(self):
        bookings = load_bookings_from_csv()  # Get all the bookings from CSV
        for booking in bookings:
            # Insert each booking as a row into the treeview
            self.tree.insert("", "end", values=(
                booking.bookingID, 
                booking.userName, 
                booking.vehicle.__class__.__name__, 
                booking.pickup, 
                booking.drop_off, 
                f"{booking.distance_km:.1f}",  # Distance rounded to 1 decimal place
                f"{booking.totalCost:.2f}"  # Total cost rounded to 2 decimal places
            ))

# Main function to run the Tkinter app
def main():
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
