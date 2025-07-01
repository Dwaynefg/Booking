import csv
import os
from pathlib import Path
from distance_calculator import DistanceCalculator

class FareCalculator:
    """Handles fare calculations for the ride booking app"""
    
    # Default vehicle data (fallback if CSV is not available)
    DEFAULT_VEHICLE_DATA = {
        "Car(4 Seater)": {"price": 100, "color": "#9C9C9C", "cost_per_km": 15, "tax": 3},
        "Car(6 Seater)": {"price": 120, "color": "#9C9C9C", "cost_per_km": 17, "tax": 3},
        "Mini Van": {"price": 200, "color": "#9C9C9C", "cost_per_km": 17, "tax": 3},
        "Van": {"price": 250, "color": "#9C9C9C", "cost_per_km": 20, "tax": 3},
        "Motorcycle": {"price": 50, "color": "#9C9C9C", "cost_per_km": 10, "tax": 3}
    }
    
    # Vehicle data loaded from CSV
    VEHICLE_DATA = {}
    
    # Pricing configuration
    MINIMUM_FARE = 50  # Minimum fare amount
    SURGE_MULTIPLIER = 1.0  # Base surge multiplier (can be adjusted for peak hours)
    
    # Payment method fees
    PAYMENT_FEES = {
        "Cash": 0,  # No additional fee for cash
        "Online Payment": 5  # 5 peso convenience fee for online payment
    }
    
    # CSV file path
    CSV_FILE_PATH = "Vehicles.csv"
    
    @classmethod
    def load_vehicle_data_from_csv(cls, csv_file_path=None):
        """
        Load vehicle data from CSV file
        
        Args:
            csv_file_path: Path to the CSV file (optional, uses default if not provided)
        """
        if csv_file_path is None:
            csv_file_path = cls.CSV_FILE_PATH
        
        try:
            # Check if file exists
            if not os.path.exists(csv_file_path):
                # Try to find the file in the current directory or parent directories
                current_dir = Path.cwd()
                possible_paths = [
                    current_dir / csv_file_path,
                    current_dir.parent / csv_file_path,
                    Path(__file__).parent / csv_file_path
                ]
                
                csv_file_path = None
                for path in possible_paths:
                    if path.exists():
                        csv_file_path = str(path)
                        break
                
                if csv_file_path is None:
                    print(f"Warning: CSV file not found. Using default vehicle data.")
                    cls.VEHICLE_DATA = cls.DEFAULT_VEHICLE_DATA.copy()
                    return False
            
            # Read CSV file with UTF-8 BOM handling
            with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Clear existing data
                cls.VEHICLE_DATA = {}
                
                # Get the actual column names (in case of BOM or spacing issues)
                fieldnames = [name.strip() for name in reader.fieldnames]
                print(f"CSV columns found: {fieldnames}")
                
                # Create a mapping for column names (handle variations)
                column_mapping = {}
                for field in fieldnames:
                    clean_field = field.strip().replace('\ufeff', '')
                    if 'vehicle' in clean_field.lower() and 'type' in clean_field.lower():
                        column_mapping['vehicle_type'] = field
                    elif 'base' in clean_field.lower() and 'fare' in clean_field.lower():
                        column_mapping['base_fare'] = field
                    elif clean_field.lower() == 'tax':
                        column_mapping['tax'] = field
                    elif 'cost' in clean_field.lower() and 'km' in clean_field.lower():
                        column_mapping['cost_km'] = field
                
                print(f"Column mapping: {column_mapping}")
                
                # Process each row
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Use mapped column names
                        vehicle_type = row[column_mapping['vehicle_type']].strip()
                        base_fare = float(row[column_mapping['base_fare']])
                        tax = float(row[column_mapping['tax']])
                        cost_per_km = float(row[column_mapping['cost_km']])
                        
                        # Store vehicle data
                        cls.VEHICLE_DATA[vehicle_type] = {
                            "price": int(base_fare),
                            "color": "#9C9C9C",  # Default color, can be customized
                            "cost_per_km": cost_per_km,
                            "tax": tax
                        }
                        
                        print(f"Loaded: {vehicle_type} - Base: ₱{base_fare}, Tax: ₱{tax}, Cost/km: ₱{cost_per_km}")
                        
                    except (ValueError, KeyError) as e:
                        print(f"Error processing row {row_num} {row}: {e}")
                        continue
                
                # Fallback to default if no data was loaded
                if not cls.VEHICLE_DATA:
                    print("Warning: No valid vehicle data found in CSV. Using default data.")
                    cls.VEHICLE_DATA = cls.DEFAULT_VEHICLE_DATA.copy()
                    return False
                
                print(f"Successfully loaded {len(cls.VEHICLE_DATA)} vehicle types from CSV")
                return True
                
        except Exception as e:
            print(f"Error loading vehicle data from CSV: {e}")
            print("Using default vehicle data.")
            cls.VEHICLE_DATA = cls.DEFAULT_VEHICLE_DATA.copy()
            return False
    
    @classmethod
    def get_vehicle_data(cls):
        """Get all vehicle data"""
        # Load from CSV if not already loaded
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        return cls.VEHICLE_DATA.copy()
    
    @classmethod
    def get_vehicle_base_price(cls, vehicle_name):
        """Get base price for a specific vehicle"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        return cls.VEHICLE_DATA.get(vehicle_name, {}).get("price", 0)
    
    @classmethod
    def get_vehicle_cost_per_km(cls, vehicle_name):
        """Get cost per kilometer for a specific vehicle"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        return cls.VEHICLE_DATA.get(vehicle_name, {}).get("cost_per_km", 10)
    
    @classmethod
    def get_vehicle_tax(cls, vehicle_name):
        """Get tax amount for a specific vehicle"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        return cls.VEHICLE_DATA.get(vehicle_name, {}).get("tax", 0)
    
    @classmethod
    def get_vehicle_color(cls, vehicle_name):
        """Get color for a specific vehicle"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        return cls.VEHICLE_DATA.get(vehicle_name, {}).get("color", "#9C9C9C")
    
    @classmethod
    def is_valid_vehicle(cls, vehicle_name):
        """Check if vehicle name is valid"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        return vehicle_name in cls.VEHICLE_DATA
    
    @classmethod
    def calculate_distance_fare(cls, vehicle_name, distance_km):
        """
        Calculate fare based on distance using vehicle-specific cost per km
        
        Args:
            vehicle_name: Name of the vehicle type
            distance_km: Distance in kilometers
            
        Returns:
            Distance fare amount
        """
        if distance_km <= 0:
            return 0
        
        cost_per_km = cls.get_vehicle_cost_per_km(vehicle_name)
        return int(distance_km * cost_per_km)
    
    @classmethod
    def calculate_base_fare(cls, vehicle_name, pickup_coords=None, dropoff_coords=None):
        """
        Calculate base fare (vehicle price + distance fare + tax)
        
        Args:
            vehicle_name: Name of selected vehicle
            pickup_coords: Tuple of (lat, lng) for pickup location
            dropoff_coords: Tuple of (lat, lng) for dropoff location
            
        Returns:
            Base fare amount in pesos
        """
        try:
            # Get vehicle base price and tax
            base_price = cls.get_vehicle_base_price(vehicle_name)
            tax = cls.get_vehicle_tax(vehicle_name)
            
            # Calculate distance fare if coordinates are provided
            distance_fare = 0
            if pickup_coords and dropoff_coords:
                distance_km = DistanceCalculator.calculate_distance_km(
                    pickup_coords[0], pickup_coords[1], 
                    dropoff_coords[0], dropoff_coords[1]
                )
                distance_fare = cls.calculate_distance_fare(vehicle_name, distance_km)
            
            total_fare = base_price + distance_fare + tax
            
            # Apply minimum fare
            return max(total_fare, cls.MINIMUM_FARE)
            
        except Exception as e:
            print(f"Error calculating base fare: {e}")
            return cls.MINIMUM_FARE
    
    @classmethod
    def calculate_payment_fee(cls, payment_method):
        """Calculate additional fee based on payment method"""
        return cls.PAYMENT_FEES.get(payment_method, 0)
    
    @classmethod
    def apply_surge_pricing(cls, base_fare, surge_multiplier=None):
        """Apply surge pricing to base fare"""
        if surge_multiplier is None:
            surge_multiplier = cls.SURGE_MULTIPLIER
        
        return int(base_fare * surge_multiplier)
    
    @classmethod
    def calculate_final_fare(cls, vehicle_name, payment_method="Cash", 
                           pickup_coords=None, dropoff_coords=None, 
                           surge_multiplier=None):
        """
        Calculate final fare including all fees and surges
        
        Args:
            vehicle_name: Name of selected vehicle
            payment_method: Payment method ("Cash" or "Online Payment")
            pickup_coords: Tuple of (lat, lng) for pickup location
            dropoff_coords: Tuple of (lat, lng) for dropoff location
            surge_multiplier: Custom surge multiplier (optional)
            
        Returns:
            Dictionary with fare breakdown
        """
        try:
            # Calculate base fare
            base_fare = cls.calculate_base_fare(vehicle_name, pickup_coords, dropoff_coords)
            
            # Apply surge pricing
            surge_fare = cls.apply_surge_pricing(base_fare, surge_multiplier)
            
            # Calculate payment fee
            payment_fee = cls.calculate_payment_fee(payment_method)
            
            # Calculate final total
            final_total = surge_fare + payment_fee
            
            # Calculate distance info
            distance_km = 0
            distance_fare = 0
            if pickup_coords and dropoff_coords:
                distance_km = DistanceCalculator.calculate_distance_km(
                    pickup_coords[0], pickup_coords[1], 
                    dropoff_coords[0], dropoff_coords[1]
                )
                distance_fare = cls.calculate_distance_fare(vehicle_name, distance_km)
            
            return {
                "vehicle_base_price": cls.get_vehicle_base_price(vehicle_name),
                "vehicle_tax": cls.get_vehicle_tax(vehicle_name),
                "cost_per_km": cls.get_vehicle_cost_per_km(vehicle_name),
                "distance_km": round(distance_km, 2),
                "distance_fare": distance_fare,
                "base_fare": base_fare,
                "surge_multiplier": surge_multiplier or cls.SURGE_MULTIPLIER,
                "surge_fare": surge_fare,
                "payment_method": payment_method,
                "payment_fee": payment_fee,
                "final_total": final_total
            }
            
        except Exception as e:
            print(f"Error calculating final fare: {e}")
            return {
                "vehicle_base_price": cls.get_vehicle_base_price(vehicle_name),
                "vehicle_tax": cls.get_vehicle_tax(vehicle_name),
                "cost_per_km": cls.get_vehicle_cost_per_km(vehicle_name),
                "distance_km": 0,
                "distance_fare": 0,
                "base_fare": cls.MINIMUM_FARE,
                "surge_multiplier": 1.0,
                "surge_fare": cls.MINIMUM_FARE,
                "payment_method": payment_method,
                "payment_fee": 0,
                "final_total": cls.MINIMUM_FARE
            }
    
    @classmethod
    def format_fare_breakdown(cls, fare_data):
        """Format fare breakdown for display"""
        try:
            breakdown = []
            breakdown.append(f"🚗 Vehicle Base Price: ₱{fare_data['vehicle_base_price']}")
            
            if fare_data.get('vehicle_tax', 0) > 0:
                breakdown.append(f"🏛️ Tax: ₱{fare_data['vehicle_tax']}")
            
            if fare_data['distance_km'] > 0:
                breakdown.append(f"📏 Distance: {fare_data['distance_km']} km")
                breakdown.append(f"🛣️ Distance Fare (₱{fare_data['cost_per_km']}/km): ₱{fare_data['distance_fare']}")
            
            if fare_data['surge_multiplier'] != 1.0:
                breakdown.append(f"⚡ Surge Multiplier: {fare_data['surge_multiplier']}x")
                breakdown.append(f"📈 Surge Fare: ₱{fare_data['surge_fare']}")
            
            if fare_data['payment_fee'] > 0:
                breakdown.append(f"💳 Payment Fee ({fare_data['payment_method']}): ₱{fare_data['payment_fee']}")
            
            breakdown.append(f"💰 Final Total: ₱{fare_data['final_total']}")
            
            return "\n".join(breakdown)
            
        except Exception as e:
            print(f"Error formatting fare breakdown: {e}")
            return f"💰 Total: ₱{fare_data.get('final_total', 0)}"
    
    @classmethod
    def get_fare_estimate_text(cls, vehicle_name, distance_km=0):
        """Get simple fare estimate text for UI display"""
        try:
            base_price = cls.get_vehicle_base_price(vehicle_name)
            tax = cls.get_vehicle_tax(vehicle_name)
            distance_fare = cls.calculate_distance_fare(vehicle_name, distance_km)
            total = max(base_price + tax + distance_fare, cls.MINIMUM_FARE)
            
            if distance_km > 0:
                cost_per_km = cls.get_vehicle_cost_per_km(vehicle_name)
                return f"₱{total} (₱{base_price} + ₱{tax} tax + ₱{distance_fare} distance @ ₱{cost_per_km}/km)"
            else:
                return f"₱{total} (₱{base_price} + ₱{tax} tax)"
                
        except Exception as e:
            print(f"Error getting fare estimate: {e}")
            return f"₱{cls.MINIMUM_FARE}"
    
    @classmethod
    def reload_vehicle_data(cls):
        """Reload vehicle data from CSV file"""
        return cls.load_vehicle_data_from_csv()
    
    @classmethod
    def get_vehicle_info(cls, vehicle_name):
        """Get complete information about a specific vehicle"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        
        return cls.VEHICLE_DATA.get(vehicle_name, {})
    
    @classmethod
    def list_available_vehicles(cls):
        """Get list of all available vehicle types"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        
        return list(cls.VEHICLE_DATA.keys())
    
    @classmethod
    def update_surge_multiplier(cls, new_multiplier):
        """Update the surge multiplier (for peak hours, etc.)"""
        if new_multiplier > 0:
            cls.SURGE_MULTIPLIER = new_multiplier
            return True
        return False
    
    @classmethod
    def get_current_surge_multiplier(cls):
        """Get current surge multiplier"""
        return cls.SURGE_MULTIPLIER
    
    @classmethod
    def add_vehicle_type(cls, vehicle_name, base_price, cost_per_km, tax=0, color="#9C9C9C"):
        """Add a new vehicle type"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        
        cls.VEHICLE_DATA[vehicle_name] = {
            "price": base_price, 
            "color": color,
            "cost_per_km": cost_per_km,
            "tax": tax
        }
    
    @classmethod
    def remove_vehicle_type(cls, vehicle_name):
        """Remove a vehicle type"""
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        
        if vehicle_name in cls.VEHICLE_DATA:
            del cls.VEHICLE_DATA[vehicle_name]
            return True
        return False
    
    @classmethod
    def update_vehicle_info(cls, vehicle_name, **kwargs):
        """
        Update vehicle information
        
        Args:
            vehicle_name: Name of the vehicle
            **kwargs: Fields to update (price, cost_per_km, tax, color)
        """
        if not cls.VEHICLE_DATA:
            cls.load_vehicle_data_from_csv()
        
        if vehicle_name in cls.VEHICLE_DATA:
            for key, value in kwargs.items():
                if key in ['price', 'cost_per_km', 'tax', 'color']:
                    cls.VEHICLE_DATA[vehicle_name][key] = value
            return True
        return False

# Auto-load vehicle data when module is imported
FareCalculator.load_vehicle_data_from_csv()