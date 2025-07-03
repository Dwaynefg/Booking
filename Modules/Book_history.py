import csv
import os
from typing import Dict, List, Optional

class BookingHistory:
    """Manages booking history storage and retrieval"""
    
    def __init__(self, csv_file: str = "Book_history.csv"):
        self.csv_file = csv_file
        self.fieldnames = [
            'Driver_name',
            'Vehicle',
            'Pickup_point',
            'Destination',
            'Distance', 
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
                          price: str = "", distance: str = "") -> bool:
        """
        Add a booking record to the CSV file
        
        Args:
            booking_details: Dictionary containing booking information
            status: Booking status (default: "Confirmed")
            price: Booking price
            distance: Pre-calculated distance string
            
        Returns:
            True if successfully added, False otherwise
        """
        try:
            # Extract driver information
            driver_info = booking_details.get('driver', {})
            
            if isinstance(driver_info, dict):
                driver_name = driver_info.get('driver_name', driver_info.get('name', ''))
                vehicle_name = driver_info.get('vehicle_name', driver_info.get('vehicle', ''))
            else:
                driver_name = str(driver_info) if driver_info else ''
                vehicle_name = ''
            
            # Use provided distance or fallback to booking_details
            final_distance = distance or booking_details.get('distance', '')
            
            # Prepare the record with only CSV fields
            record = {
                'Driver_name': driver_name,
                'Vehicle': vehicle_name,
                'Pickup_point': booking_details.get('pickup_location', booking_details.get('pickup_point', '')),
                'Destination': booking_details.get('dropoff_location', booking_details.get('destination', '')),
                'Distance': final_distance,
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
        """
        Update the status of an existing booking
        
        Args:
            booking_id: Booking ID to update
            new_status: New status ("Confirmed", "Cancelled", "Finished")
            
        Returns:
            True if successfully updated, False otherwise
        """
        try:
            records = []
            updated = False
            
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Booking_ID'] == booking_id:
                        row['Status'] = new_status
                        updated = True
                    records.append(row)
            
            if updated:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(records)
                
                print(f"✅ Updated booking {booking_id} status to {new_status}")
                return True
            else:
                print(f"⚠️ Booking {booking_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error updating booking status: {e}")
            return False
    
    def update_booking_distance(self, booking_id: str, new_distance: str) -> bool:
        """
        Update the distance for an existing booking
        
        Args:
            booking_id: Booking ID to update
            new_distance: New distance string
            
        Returns:
            True if successfully updated, False otherwise
        """
        try:
            records = []
            updated = False
            
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Booking_ID'] == booking_id:
                        row['Distance'] = new_distance
                        updated = True
                    records.append(row)
            
            if updated:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(records)
                
                print(f"✅ Updated booking {booking_id} distance to {new_distance}")
                return True
            else:
                print(f"⚠️ Booking {booking_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error updating booking distance: {e}")
            return False
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Dict]:
        """Get a specific booking record by ID"""
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Booking_ID'] == booking_id:
                        return row
            return None
            
        except Exception as e:
            print(f"❌ Error getting booking by ID: {e}")
            return None
    
    def get_all_bookings(self) -> List[Dict]:
        """Get all booking records"""
        try:
            records = []
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                records = list(reader)
            return records
            
        except Exception as e:
            print(f"❌ Error getting all bookings: {e}")
            return []
    
    def get_bookings_by_status(self, status: str) -> List[Dict]:
        """Get booking records by status"""
        try:
            filtered_records = []
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Status'].lower() == status.lower():
                        filtered_records.append(row)
            return filtered_records
            
        except Exception as e:
            print(f"❌ Error getting bookings by status: {e}")
            return []
    
    def get_bookings_by_driver(self, driver_name: str) -> List[Dict]:
        """Get booking records by driver name"""
        try:
            filtered_records = []
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Driver_name'].lower() == driver_name.lower():
                        filtered_records.append(row)
            return filtered_records
            
        except Exception as e:
            print(f"❌ Error getting bookings by driver: {e}")
            return []
    
    def get_booking_statistics(self) -> Dict:
        """Get basic booking statistics including distance analysis"""
        try:
            records = self.get_all_bookings()
            total_bookings = len(records)
            
            status_counts = {}
            driver_counts = {}
            vehicle_counts = {}
            total_distance_km = 0
            distance_count = 0
            
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
                
                # Calculate total distance if format is parseable
                distance_str = record.get('Distance', '')
                if distance_str and 'km' in distance_str:
                    try:
                        # Extract km value from formatted string like "5.23 km"
                        km_value = float(distance_str.split(' km')[0])
                        total_distance_km += km_value
                        distance_count += 1
                    except (ValueError, IndexError):
                        pass
            
            avg_distance_km = total_distance_km / distance_count if distance_count > 0 else 0
            
            return {
                'total_bookings': total_bookings,
                'status_counts': status_counts,
                'driver_counts': driver_counts,
                'vehicle_counts': vehicle_counts,
                'total_distance_km': round(total_distance_km, 2),
                'average_distance_km': round(avg_distance_km, 2),
                'bookings_with_distance': distance_count
            }
            
        except Exception as e:
            print(f"❌ Error getting booking statistics: {e}")
            return {
                'total_bookings': 0,
                'status_counts': {},
                'driver_counts': {},
                'vehicle_counts': {},
                'total_distance_km': 0,
                'average_distance_km': 0,
                'bookings_with_distance': 0
            }
    
    def format_booking_record(self, record: Dict) -> str:
        """Format a booking record for display"""
        return f"""📋 Booking ID: {record.get('Booking_ID', 'N/A')}
👨‍✈️ Driver: {record.get('Driver_name', 'N/A')}
🚗 Vehicle: {record.get('Vehicle', 'N/A')}
📍 Route: {record.get('Pickup_point', 'N/A')} → {record.get('Destination', 'N/A')}
📏 Distance: {record.get('Distance', 'N/A')}
💰 Price: {record.get('Price', 'N/A')}
📊 Status: {record.get('Status', 'N/A')}"""
    
    def delete_booking_record(self, booking_id: str) -> bool:
        """Delete a booking record by ID"""
        try:
            records = []
            deleted = False
            
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Booking_ID'] != booking_id:
                        records.append(row)
                    else:
                        deleted = True
            
            if deleted:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                    writer.writeheader()
                    writer.writerows(records)
                
                print(f"✅ Deleted booking record: {booking_id}")
                return True
            else:
                print(f"⚠️ Booking {booking_id} not found")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting booking record: {e}")
            return False
    
    def clear_all_records(self) -> bool:
        """Clear all booking records (keep headers)"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
            
            print("✅ Cleared all booking records")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing records: {e}")
            return False