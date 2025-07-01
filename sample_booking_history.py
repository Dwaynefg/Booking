import customtkinter as ctk
import pandas as pd
import os

# Set up the main window
ctk.set_appearance_mode("System")  # or "Dark", "Light"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Booking History")
root.geometry("1000x600")

# Create a frame to hold the scrollable content
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Create a CTkScrollableFrame
scrollable_frame = ctk.CTkScrollableFrame(frame)
scrollable_frame.pack(fill="both", expand=True)

# Function to read the CSV and return the data using pandas
def read_booking_data(filename):
    try:
        # Check if the filename has a '.csv' extension, if not, append it
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Print current directory to check where the script is looking for the file
        print("Current working directory:", os.getcwd())
        
        # Attempt to read the file
        print(f"Attempting to read file: {filename}")
        
        # Check if file exists before trying to read it
        if not os.path.exists(filename):
            print(f"Error: {filename} does not exist.")
            return None
        
        df = pd.read_csv("booking_history.csv")
        
        # If the dataframe is empty, return None
        if df is None or df.empty:
            print("The file is empty or could not be read.")
            return None
        else:
            print("Data loaded successfully:")
            print(df.head())  # Show the first few rows of the DataFrame for debugging
            return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

# Read data from CSV file (ensure the file name is correct)
bookings_df = read_booking_data("booking_history.csv")  # Assuming the CSV file is named 'booking_history.csv'

# Check if the data is loaded successfully
if bookings_df is not None:
    print("Bookings data loaded successfully:")
    print(bookings_df.head())  # Print the first few rows
else:
    print("No bookings found!")

# Add column headers to the Scrollable Frame
header_frame = ctk.CTkFrame(scrollable_frame)
header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

# Column headers from the DataFrame
header_labels = bookings_df.columns.tolist()

# Adding the headers (only once for the header)
for col, header in enumerate(header_labels):
    header_label = ctk.CTkLabel(header_frame, text=header, width=15, anchor="w")
    header_label.grid(row=0, column=col, padx=10)

# Add booking data to the scrollable frame (starting from row 1)
for i, row in bookings_df.iterrows():
    row_frame = ctk.CTkFrame(scrollable_frame)
    row_frame.grid(row=i + 1, column=0, padx=20, pady=10, sticky="w")

    # Add each field in the row (Booking Data)
    for col, value in enumerate(row):
        data_label = ctk.CTkLabel(row_frame, text=value, width=15, anchor="w")
        data_label.grid(row=0, column=col, padx=10)

# Run the main loop to display the window
root.mainloop()
