import csv
import random
from typing import Dict, List, Optional, Tuple

class Driver:
    """Represents a driver with their vehicle information"""
    
    def __init__(self, vehicle_type: str, driver_name: str, vehicle_name: str, 
                 contact_no: str, plate_no: str, status: str = "available"):
        self.vehicle_type = vehicle_type
        self.driver_name = driver_name
        self.vehicle_name = vehicle_name
        self.contact_no = contact_no
        self.plate_no = plate_no
        self.status = status.lower().strip()  # Store status from CSV
        self.is_available = self.status == "available"  # Set availability based on status
    
    def __str__(self):
        return f"{self.driver_name} - {self.vehicle_name} ({self.plate_no}) - {self.status}"
    
    def to_dict(self):
        """Convert driver to dictionary for easy access"""
        return {
            'vehicle_type': self.vehicle_type,
            'driver_name': self.driver_name,
            'vehicle_name': self.vehicle_name,
            'contact_no': self.contact_no,
            'plate_no': self.plate_no,
            'status': self.status,
            'is_available': self.is_available
        }
    
    def set_status(self, status: str):
        """Update driver status"""
        self.status = status.lower().strip()
        self.is_available = self.status == "available"
    
    def assign(self):
        """Mark driver as assigned"""
        self.set_status("assigned")
    
    def make_available(self):
        """Mark driver as available"""
        self.set_status("available")
    
    def set_unavailable(self, reason: str = "unavailable"):
        """Mark driver as unavailable with optional reason"""
        self.set_status(reason)

class DriverManager:
    """Manages driver data and assignments"""
    
    def __init__(self, csv_file: str = "driver.csv"):
        self.csv_file = csv_file
        self.drivers_by_type: Dict[str, List[Driver]] = {}
        self.all_drivers: List[Driver] = []
        self.assigned_drivers: Dict[str, Driver] = {}  # Track assigned drivers by booking ID
        
        # Load drivers from CSV
        self.load_drivers()
    
    def load_drivers(self):
        """Load drivers from CSV file and organize by vehicle type"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    # Get status from CSV, default to "available" if not present
                    status = row.get('status', 'available').strip()
                    
                    driver = Driver(
                        vehicle_type=row['Vehicle_Type'].strip(),
                        driver_name=row['driver_name'].strip(),
                        vehicle_name=row['vehicle_name'].strip(),
                        contact_no=row['contact_no'].strip(),
                        plate_no=row['plate_no'].strip(),
                        status=status
                    )
                    
                    # Add to all drivers list
                    self.all_drivers.append(driver)
                    
                    # Organize by vehicle type
                    if driver.vehicle_type not in self.drivers_by_type:
                        self.drivers_by_type[driver.vehicle_type] = []
                    
                    self.drivers_by_type[driver.vehicle_type].append(driver)
            
            print(f"Successfully loaded {len(self.all_drivers)} drivers")
            self.print_driver_summary()
            
        except FileNotFoundError:
            print(f"Error: {self.csv_file} not found!")
        except Exception as e:
            print(f"Error loading drivers: {e}")
    
    def print_driver_summary(self):
        """Print summary of drivers by vehicle type and status"""
        print("\n--- Driver Summary ---")
        for vehicle_type, drivers in self.drivers_by_type.items():
            available_count = sum(1 for d in drivers if d.is_available)
            total_count = len(drivers)
            unavailable_count = total_count - available_count
            
            print(f"{vehicle_type}: {total_count} total ({available_count} available, {unavailable_count} unavailable)")
            
            # Show status breakdown
            status_counts = {}
            for driver in drivers:
                status = driver.status
                status_counts[status] = status_counts.get(status, 0) + 1
            
            status_breakdown = ", ".join([f"{count} {status}" for status, count in status_counts.items()])
            print(f"  Status breakdown: {status_breakdown}")
    
    def get_available_vehicle_types(self) -> List[str]:
        """Get list of available vehicle types"""
        return list(self.drivers_by_type.keys())
    
    def get_drivers_by_type(self, vehicle_type: str) -> List[Driver]:
        """Get all drivers for a specific vehicle type"""
        return self.drivers_by_type.get(vehicle_type, [])
    
    def get_available_drivers_by_type(self, vehicle_type: str) -> List[Driver]:
        """Get available drivers for a specific vehicle type"""
        drivers = self.drivers_by_type.get(vehicle_type, [])
        return [driver for driver in drivers if driver.is_available]
    
    def get_drivers_by_status(self, vehicle_type: str, status: str) -> List[Driver]:
        """Get drivers by vehicle type and status"""
        drivers = self.drivers_by_type.get(vehicle_type, [])
        return [driver for driver in drivers if driver.status == status.lower().strip()]
    
    def assign_random_driver(self, vehicle_type: str, booking_id: str = None, auto_save: bool = True) -> Optional[Driver]:
        available_drivers = self.get_available_drivers_by_type(vehicle_type)
    
        if not available_drivers:
            print(f"No available drivers for {vehicle_type}")
            return None
    
        # Randomly select a driver
        selected_driver = random.choice(available_drivers)
    
        # Mark driver as assigned (not busy yet)
        selected_driver.assign()
    
        # Track assignment if booking ID provided
        if booking_id:
            self.assigned_drivers[booking_id] = selected_driver
    
        # Auto-save to CSV if enabled
        if auto_save:
            try:
                self.save_drivers_to_csv()
                print(f"Driver assignment saved to {self.csv_file}")
            except Exception as e:
                print(f"Warning: Could not save driver status to CSV: {e}")
    
        print(f"Assigned driver: {selected_driver}")
        return selected_driver
    
    def release_driver(self, booking_id: str = None, driver: Driver = None):
        
        if booking_id and booking_id in self.assigned_drivers:
            driver = self.assigned_drivers.pop(booking_id)
            driver.make_available()
            print(f"Released driver: {driver}")
        elif driver:
            driver.make_available()
            print(f"Released driver: {driver}")

    def release_driver_to_available(self, booking_id: str):
        """Release driver back to available status and save to CSV"""
        if booking_id in self.assigned_drivers:
            driver = self.assigned_drivers.pop(booking_id)
            driver.make_available()
        
            # Save to CSV immediately
            try:
                self.save_drivers_to_csv()
                print(f"Driver {driver.driver_name} marked as available and saved to CSV")
            except Exception as e:
                print(f"Error saving driver available status: {e}")
        
            return driver
        return None
    
    def set_driver_busy(self, booking_id: str):
        """Mark driver as busy and save to CSV"""
        if booking_id in self.assigned_drivers:
            driver = self.assigned_drivers[booking_id]
            driver.set_status("busy")
        
            # Save to CSV immediately
            try:
                self.save_drivers_to_csv()
                print(f"Driver {driver.driver_name} marked as busy and saved to CSV")
            except Exception as e:
                print(f"Error saving driver busy status: {e}")
    
    def get_assigned_driver(self, booking_id: str) -> Optional[Driver]:
        """Get the driver assigned to a specific booking"""
        return self.assigned_drivers.get(booking_id)
    
    def get_driver_count_by_type(self, vehicle_type: str) -> Tuple[int, int]:
        
        total_drivers = len(self.drivers_by_type.get(vehicle_type, []))
        available_drivers = len(self.get_available_drivers_by_type(vehicle_type))
        return total_drivers, available_drivers
    
    def get_status_counts_by_type(self, vehicle_type: str) -> Dict[str, int]:
        
        drivers = self.drivers_by_type.get(vehicle_type, [])
        status_counts = {}
        
        for driver in drivers:
            status = driver.status
            status_counts[status] = status_counts.get(status, 0) + 1
            
        return status_counts
    
    def reset_all_drivers(self):
        """Reset all drivers to available status"""
        for driver in self.all_drivers:
            driver.make_available()
        self.assigned_drivers.clear()
        print("All drivers reset to available status")
    
    def get_driver_info(self, vehicle_type: str) -> str:
        """Get formatted driver information for a vehicle type"""
        total, available = self.get_driver_count_by_type(vehicle_type)
        return f"{available}/{total} drivers available"
    
    def get_detailed_driver_info(self, vehicle_type: str) -> str:
        """Get detailed driver information including status breakdown"""
        status_counts = self.get_status_counts_by_type(vehicle_type)
        total = sum(status_counts.values())
        
        if not status_counts:
            return f"No drivers found for {vehicle_type}"
        
        available = status_counts.get('available', 0)
        info = f"{available}/{total} drivers available"
        
        # Add status breakdown if there are unavailable drivers
        if total > available:
            other_statuses = []
            for status, count in status_counts.items():
                if status != 'available':
                    other_statuses.append(f"{count} {status}")
            
            if other_statuses:
                info += f" ({', '.join(other_statuses)})"
        
        return info

    def book_ride(self, vehicle_type: str, pickup_location: str, dropoff_location: str) -> Optional[Dict]:
        import uuid
    
        # Generate unique booking ID
        booking_id = str(uuid.uuid4())[:8]
    
        # Assign a driver (without auto-save)
        assigned_driver = self.assign_random_driver(vehicle_type, booking_id, auto_save=False)
    
        if not assigned_driver:
            return None
    
        # Create booking details (driver is still "assigned" at this point)
        booking_details = {
            'booking_id': booking_id,
            'vehicle_type': vehicle_type,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'driver': assigned_driver.to_dict(),
            'status': 'confirmed'
        }
    
        return booking_details
    
    def update_driver_status(self, plate_no: str, new_status: str) -> bool:
        """
        Update a specific driver's status by plate number
        
        Args:
            plate_no: Driver's plate number
            new_status: New status to set
            
        Returns:
            True if driver found and updated, False otherwise
        """
        for driver in self.all_drivers:
            if driver.plate_no == plate_no:
                old_status = driver.status
                driver.set_status(new_status)
                print(f"Updated driver {driver.driver_name} ({plate_no}) from '{old_status}' to '{new_status}'")
                return True
        
        print(f"Driver with plate number {plate_no} not found")
        return False
    
    def save_drivers_to_csv(self, output_file: str = None):
        """
        Save current driver data back to CSV file
        
        Args:
            output_file: Output CSV file path. If None, overwrites original file.
        """
        if output_file is None:
            output_file = self.csv_file
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Vehicle_Type', 'driver_name', 'vehicle_name', 'contact_no', 'plate_no', 'status']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for driver in self.all_drivers:
                    writer.writerow({
                        'Vehicle_Type': driver.vehicle_type,
                        'driver_name': driver.driver_name,
                        'vehicle_name': driver.vehicle_name,
                        'contact_no': driver.contact_no,
                        'plate_no': driver.plate_no,
                        'status': driver.status
                    })
            
            print(f"Driver data saved to {output_file}")
            
        except Exception as e:
            print(f"Error saving driver data: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Create driver manager
    manager = DriverManager()
    
    # Test driver assignment
    print("\n--- Testing Driver Assignment ---")
    
    # Assign drivers for different vehicle types
    car_driver = manager.assign_random_driver("Car(4 Seater)", "booking_001")
    van_driver = manager.assign_random_driver("Mini Van", "booking_002")
    motorcycle_driver = manager.assign_random_driver("Motorcycle", "booking_003")
    
    # Check driver availability with detailed info
    print(f"\nCar(4 Seater) - {manager.get_detailed_driver_info('Car(4 Seater)')}")
    print(f"Mini Van - {manager.get_detailed_driver_info('Mini Van')}")
    print(f"Motorcycle - {manager.get_detailed_driver_info('Motorcycle')}")
    
    # Test status update
    print("\n--- Testing Status Update ---")
    if car_driver:
        manager.update_driver_status(car_driver.plate_no, "maintenance")
        print(f"Car(4 Seater) - {manager.get_detailed_driver_info('Car(4 Seater)')}")
    
    # Test booking system
    print("\n--- Testing Booking System ---")
    booking = manager.book_ride("Car(6 Seater)", "Mall of Asia", "NAIA Terminal 3")
    if booking:
        print(f"Booking successful: {booking['booking_id']}")
        print(f"Driver: {booking['driver']['driver_name']}")
        print(f"Vehicle: {booking['driver']['vehicle_name']}")
        print(f"Contact: {booking['driver']['contact_no']}")
        print(f"Status: {booking['driver']['status']}")
    
    # Release a driver
    print("\n--- Releasing Driver ---")
    manager.release_driver("booking_002")
    print(f"Mini Van - {manager.get_detailed_driver_info('Mini Van')}")
    
    # Show final status summary
    print("\n--- Final Status Summary ---")
    manager.print_driver_summary()
    
    # Test saving to CSV
    print("\n--- Testing CSV Save ---")
    manager.save_drivers_to_csv("updated_driver.csv")