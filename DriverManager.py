import csv
import random
import os

class DriverManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.driver_data = self.load_driver_data("driver.csv")
    
    def load_driver_data(self, file_path):
        """Reads driver data from the CSV file and organizes it by vehicle type."""
        data = {
            "Car(4 Seater)": [],
            "Car(6 Seater)": [],
            "Minivan": [],
            "Van": [],
            "Mini Van": [],
            "Motorcycle": []
        }
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vehicle_type = row['Vehicle_Type']
                if vehicle_type in data:
                    data[vehicle_type].append({
                        "driver_name": row['driver_name'],
                        "vehicle_name": row['vehicle_name'],
                        "contact_no": row['contact_no'],
                        "plate_no": row['plate_no'],
                        "status": row.get('status', 'available')  # Add status field to track driver availability
                    })
                else:
                    print(f"Warning: Vehicle type '{vehicle_type}' not recognized and will be ignored.")
        return data
    
    def get_driver_info(self, Vehicle_Type):
        """Randomly pick a driver for the given vehicle type."""
        if Vehicle_Type in self.driver_data:
            available_drivers = [driver for driver in self.driver_data[Vehicle_Type] if driver['status'] == 'available']
            if available_drivers:
                return random.choice(available_drivers)
            else:
                print(f"No drivers available for vehicle type '{Vehicle_Type}'.")
                return None
        else:
            raise ValueError(f"Vehicle type '{Vehicle_Type}' is not recognized.")
    
    def update_driver_status(self, Vehicle_Type, driver_name, new_status):
        """Update the status of a driver (e.g., to 'busy' after booking)."""
        # Find and update the driver's status in the data
        for driver in self.driver_data.get(Vehicle_Type, []):
            if driver['driver_name'] == driver_name:
                driver['status'] = new_status
                break
        else:
            print(f"Driver '{driver_name}' not found for vehicle type '{Vehicle_Type}'.")
        
        # Save updated driver data back to CSV
        self.save_driver_data()
    
    def save_driver_data(self):
        """Save updated driver information back to the CSV file."""
        # Flatten the driver data back to a list of dictionaries
        flattened_data = []
        for vehicle_type, drivers in self.driver_data.items():
            for driver in drivers:
                driver_copy = driver.copy()
                driver_copy['vehicle_type'] = vehicle_type
                flattened_data.append(driver_copy)
        
        # Write the updated data to the CSV file
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['driver_name', 'vehicle_name', 'contact_no', 'plate_no', 'vehicle_type', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_data)
