import pandas as pd
from tkinter import ttk
import customtkinter as ctk

class CSVViewer(ctk.CTkFrame):
    def __init__(self, parent, csv_file):
        super().__init__(parent)
        self.csv_file = csv_file
        
        # Create treeview
        self.tree = ttk.Treeview(self)
        
        # Configure scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load data
        self.load_data()
    
    def load_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Read CSV file
            df = pd.read_csv(self.csv_file)
            
            # If empty, create sample columns
            if df.empty:
                df = pd.DataFrame(columns=[
                    "ID", "User", "Vehicle", "From", "To", 
                    "Distance", "Cost", "Status"
                ])
                df.to_csv(self.csv_file, index=False)
            
            # Configure treeview columns
            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")
            
            # Insert data
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))
                
        except FileNotFoundError:
            # Create new CSV with headers if file doesn't exist
            df = pd.DataFrame(columns=[
                "ID", "User", "Vehicle", "From", "To", 
                "Distance", "Cost", "Status"
            ])
            df.to_csv(self.csv_file, index=False)
            self.load_data()  # Reload after creating file

# Example usage:
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer")
        self.geometry("1000x600")
        
        # Create CSV viewer
        self.viewer = CSVViewer(self, "ride_bookings.csv")
        self.viewer.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()