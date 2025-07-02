import csv
import os
from typing import Dict, List, Optional

class BookingHistory:
    """Manages booking history storage and retrieval (without distance calculation)"""
    
    def __init__(self, csv_file: str = "Book_history.csv"):
        self.csv_file = csv_file
        self.fieldnames = [
            'Driver_name',
            'Vehicle',
            'Pickup_point',
            'Destination',
            'Booking_ID',
            'Price',
            'Status'
        ]
        
        # Ensure CSV file exists with headers
        self.ensure_csv_exists()
    
    def ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            try:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                    writer.writeheader()
                print(f"✅ Created {self.csv_file} with headers")
            except Exception as e:
                print(f"❌ Error creating {self.csv_file}: {e}")
    
    def add_booking_record(self, booking_details: Dict, status: str = "Confirmed", 
                          price: str = "") -> bool:
        """Add a booking record without distance calculation"""
        try:
            # Extract driver information
            driver_info = booking_details.get('driver', {})
            
            if isinstance(driver_info, dict):
                driver_name = driver_info.get('driver_name', driver_info.get('name', ''))
                vehicle_name = driver_info.get('vehicle_name', driver_info.get('vehicle', ''))
            else:
                driver_name = str(driver_info) if driver_info else ''
                vehicle_name = ''
            
            # Prepare the record
            record = {
                'Driver_name': driver_name,
                'Vehicle': vehicle_name,
                'Pickup_point': booking_details.get('pickup_location', booking_details.get('pickup_point', '')),
                'Destination': booking_details.get('dropoff_location', booking_details.get('destination', '')),
                'Booking_ID': booking_details.get('booking_id', ''),
                'Price': price or booking_details.get('price', ''),
                'Status': status
            }
            
            # Write to CSV
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writerow(record)
            
            print(f"✅ Added booking record: {record['Booking_ID']} - {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding booking record: {e}")
            return False
    
    def update_booking_status(self, booking_id: str, new_status: str) -> bool:
        """Update booking status (unchanged)"""
        # ... (keep existing implementation) ...
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Dict]:
        """Get booking by ID (unchanged)"""
        # ... (keep existing implementation) ...
    
    def get_all_bookings(self) -> List[Dict]:
        """Get all bookings (unchanged)"""
        # ... (keep existing implementation) ...
    
    def get_booking_statistics(self) -> Dict:
        """Get statistics without distance metrics"""
        try:
            records = self.get_all_bookings()
            total_bookings = len(records)
            
            status_counts = {}
            driver_counts = {}
            vehicle_counts = {}
            
            for record in records:
                # Count by status
                status = record.get('Status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Count by driver
                driver = record.get('Driver_name', 'Unknown')
                if driver and driver != 'Unknown':
                    driver_counts[driver] = driver_counts.get(driver, 0) + 1
                
                # Count by vehicle
                vehicle = record.get('Vehicle', 'Unknown')
                if vehicle and vehicle != 'Unknown':
                    vehicle_counts[vehicle] = vehicle_counts.get(vehicle, 0) + 1
            
            return {
                'total_bookings': total_bookings,
                'status_counts': status_counts,
                'driver_counts': driver_counts,
                'vehicle_counts': vehicle_counts
            }
            
        except Exception as e:
            print(f"❌ Error getting booking statistics: {e}")
            return {
                'total_bookings': 0,
                'status_counts': {},
                'driver_counts': {},
                'vehicle_counts': {}
            }
    
    # ... (keep other methods unchanged) ...

# Example usage (updated):
if __name__ == "__main__":
    booking_history = BookingHistory()
    
    sample_booking = {
        'booking_id': 'BK001',
        'driver': {
            'driver_name': 'John Smith',
            'vehicle_name': 'Toyota Camry'
        },
        'pickup_location': 'Manila Airport',
        'dropoff_location': 'Makati CBD',
        'price': '₱500'
    }
    
    booking_history.add_booking_record(
        booking_details=sample_booking,
        status="Confirmed"
    )
    
    stats = booking_history.get_booking_statistics()
    print("\n📊 Booking Statistics:")
    print(f"Total Bookings: {stats['total_bookings']}")
    print(f"By Status: {stats['status_counts']}")