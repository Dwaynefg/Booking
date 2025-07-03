import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import threading
import time

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now your module imports should work
from BOOKING_PAGE.map_widget import MapWidget
from Modules.distance_calculator import DistanceCalculator
from BOOKING_PAGE.ui_manager import UIManager
from Modules.driver_management import DriverManager
from Modules.Book_history import BookingHistory
from Modules.eta_calculator import ETACalculator


# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Get the directory where this script is located
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def create_assets_folder():
    """Create assets folder if it doesn't exist"""
    ASSETS_PATH.mkdir(parents=True, exist_ok=True)

class MapWithDistanceRideBookingApp:
    def __init__(self):
        self.window = None
        self.map_widget = None
        self.ui_manager = None
        self.driver_manager = None
        self.current_booking = None
        self.booking_history = BookingHistory("Book_history.csv")
        self.cancellation_dialog = None
        self.cancellation_timer = None
        self.is_cancellation_active = False
        self.current_user = None  
        self.logout_callback = None  
        self.eta_calculator = ETACalculator()
        
        # Setup window and components
        self.setup_window()
        self.setup_components()

    def setup_logout_callback(self, callback):
        """Set up logout callback function"""
        self.logout_callback = callback

    def logout(self):
        """Handle logout functionality"""
        try:
            # Show confirmation dialog
            result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
            if result:
                # Close current window
                if self.window:
                    self.window.destroy()
                
                # Call logout callback if available
                if self.logout_callback:
                    self.logout_callback()
                else:
                    # Fallback: try to import and create login page
                    try:
                        from login_page import LoginApp
                        login_app = LoginApp()
                        login_app.run()
                    except ImportError:
                        print("Could not import login page")
        except Exception as e:
            print(f"Error during logout: {e}")

    def setup_window(self):
        """Setup the main window"""
        create_assets_folder()

        self.window = ctk.CTk()
        self.window.title("Go-Do - Modern Ride Booking App")
        self.window.state('zoomed')  # Just maximized, not fullscreen
    
        # Bind keyboard shortcuts
        self.window.bind('<F11>', self.toggle_fullscreen)
        self.window.bind('<Escape>', self.exit_fullscreen)
        self.window.bind('<Alt-Return>', self.toggle_fullscreen)

        # Add logout button to window (optional)
        self.add_logout_button()

    def add_logout_button(self):
        """Add logout button to the main window"""
        try:
            # Create a logout button in the top-right corner
            logout_btn = ctk.CTkButton(
                self.window,
                text="🚪 Logout",
                width=80,
                height=30,
                fg_color="#FF4444",
                hover_color="#CC3333",
                command=self.logout
            )
            logout_btn.place(relx=0.98, rely=0.02, anchor="ne")
        except Exception as e:
            print(f"Error adding logout button: {e}")

    def setup_components(self):
        """Setup UI components and map widget"""
        # Initialize driver manager first
        self.driver_manager = DriverManager("data/driver.csv")
        
        # Initialize UI manager with driver manager
        self.ui_manager = UIManager(self.window, self, self.driver_manager)
        
        # Create map widget - access through left_panel
        self.map_widget = MapWidget(self.ui_manager.left_panel.map_frame, parent_app=self)
        self.map_widget.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initial setup
        self.window.after(100, self.ui_manager.initial_resize)
        
    def button_click(self, button_name):
        """Handle button clicks"""
        if button_name == "book_ride":
            self.handle_book_ride()
        elif button_name == "cancel":
            self.reset_form()
        else:
            # Handle other button clicks if needed
            pass
    
    def handle_book_ride(self):
        """Handle ride booking with driver assignment"""
        pickup = self.ui_manager.get_pickup_text()
        dropoff = self.ui_manager.get_dropoff_text()

        if not pickup or not dropoff or pickup == "Enter pickup address..." or dropoff == "Enter dropoff address...":
            messagebox.showwarning("Missing Information ⚠️", "Please enter both pickup and dropoff locations")
            return

        # Get selected vehicle type
        selected_vehicle = self.ui_manager.get_selected_vehicle()
        if not selected_vehicle:
            messagebox.showwarning("No Vehicle Selected ⚠️", "Please select a vehicle type")
            return

        # Check if drivers are available for the selected vehicle type
        available_drivers = self.driver_manager.get_available_drivers_by_type(selected_vehicle)
        if not available_drivers:
            total_drivers = len(self.driver_manager.get_drivers_by_type(selected_vehicle))
            messagebox.showerror("No Drivers Available 🚫", 
                               f"Sorry, no {selected_vehicle} drivers are available right now.\n"
                               f"Total {selected_vehicle} drivers: {total_drivers}\n"
                               f"Available: 0")
            return

        # Attempt to book the ride
        booking_details = self.driver_manager.book_ride(
            vehicle_type=selected_vehicle,
            pickup_location=pickup,
            dropoff_location=dropoff
        )

        if booking_details:
            self.current_booking = booking_details
            self.show_booking_confirmation_with_cancellation(booking_details)
        else:
            messagebox.showerror("Booking Failed ❌", "Failed to book ride. Please try again.")

    def show_booking_confirmation_with_cancellation(self, booking_details):
        """Enhanced booking confirmation with ETA information"""
        driver_info = booking_details['driver']

        # Update the right panel with driver information
        self.ui_manager.right_panel.update_driver_info(driver_info)

        # Get booking information
        selected_price = self.ui_manager.get_selected_vehicle_price()
        payment_mode = self.ui_manager.get_payment_mode()
        fare_breakdown = self.ui_manager.get_fare_breakdown()

        # Calculate ETA for the booked vehicle
        eta_info = None
        pickup_pos = self.map_widget.get_pickup_position() if self.map_widget else None
        dropoff_pos = self.map_widget.get_dropoff_position() if self.map_widget else None
        
        if pickup_pos and dropoff_pos:
            vehicle = self.get_vehicle_by_type(booking_details['vehicle_type'])
            if vehicle:
                eta_info = ETACalculator.calculate_eta_for_vehicle(
                    pickup_pos[0], pickup_pos[1],
                    dropoff_pos[0], dropoff_pos[1],
                    vehicle
                )

        # *** ADD THE BOOKING TO HISTORY HERE ***
        try:
            # Get distance if available
            distance_str = ""
            if pickup_pos and dropoff_pos:
                distance_km = DistanceCalculator.calculate_distance_km(
                    pickup_pos[0], pickup_pos[1],
                    dropoff_pos[0], dropoff_pos[1]
                )
                distance_str = f"{distance_km:.2f} km"
            
            # Add to booking history
            self.booking_history.add_booking_record(
                booking_details,
                status="Confirmed",
                price=selected_price,
                distance=distance_str
            )
        except Exception as e:
            print(f"Error adding booking to history: {e}")

        # Create comprehensive booking confirmation message
        booking_message = "🎉 Ride Booked Successfully!\n\n"
        booking_message += f"📋 Booking ID: {booking_details['booking_id']}\n"
        booking_message += f"📍 From: {booking_details['pickup_location']}\n"
        booking_message += f"📍 To: {booking_details['dropoff_location']}\n\n"

        booking_message += "👨‍✈️ Driver Details:\n"
        booking_message += f"• Name: {driver_info['driver_name']}\n"
        booking_message += f"• Vehicle: {driver_info['vehicle_name']}\n"
        booking_message += f"• Plate: {driver_info['plate_no']}\n"
        booking_message += f"• Contact: {driver_info['contact_no']}\n\n"

        booking_message += f"🚗 Vehicle Type: {booking_details['vehicle_type']}\n"

        # Add ETA information
        if eta_info and eta_info['eta_minutes'] > 0:
            booking_message += f"\n⏱️ Estimated Travel Time: {eta_info['eta_formatted']}\n"
            
            if eta_info.get("arrival_time"):
                arrival_text = ETACalculator.format_arrival_time(eta_info["arrival_time"])
                booking_message += f"🎯 Expected Arrival: {arrival_text}\n"

        if selected_price:
            booking_message += f"💰 Price: {selected_price}\n"

        if payment_mode:
            booking_message += f"💳 Payment: {payment_mode}\n"

        if fare_breakdown and fare_breakdown != "No fare information available":
            booking_message += f"\n📊 Fare Breakdown:\n{fare_breakdown}\n"

        booking_message += "\n🚗 Your driver will arrive shortly!"

        # Show confirmation
        messagebox.showinfo("Booking Confirmed ✅", booking_message)

        # *** MARK DRIVER AS BUSY AND SAVE TO CSV ***
        booking_id = booking_details['booking_id']
        self.driver_manager.set_driver_busy(booking_id)

        # Start the 15-second cancellation window
        self.start_cancellation_window()

    def start_cancellation_window(self):
        """Start the 15-second cancellation window"""
        if self.is_cancellation_active:
            return  # Prevent multiple cancellation windows
            
        self.is_cancellation_active = True
        
        try:
            # Create cancellation dialog
            self.cancellation_dialog = ctk.CTkToplevel(self.window)
            self.cancellation_dialog.title("⏰ Cancellation Window")
            self.cancellation_dialog.geometry("450x300")
            self.cancellation_dialog.transient(self.window)
            self.cancellation_dialog.grab_set()
            
            # Make dialog always on top
            self.cancellation_dialog.attributes('-topmost', True)
            
            # Center the dialog
            self.cancellation_dialog.geometry("+%d+%d" % (
                self.window.winfo_rootx() + 100,
                self.window.winfo_rooty() + 100
            ))
            
            # Main frame
            main_frame = ctk.CTkFrame(self.cancellation_dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = ctk.CTkLabel(
                main_frame,
                text="⏰ Cancellation Window",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            title_label.pack(pady=(15, 10))
            
            # Info text
            info_text = ("You have 15 seconds to cancel this ride\n"
                        "if you change your mind.\n\n"
                        "After this window closes, cancellation\n"
                        "may incur additional charges.")
            
            info_label = ctk.CTkLabel(
                main_frame,
                text=info_text,
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            info_label.pack(pady=(0, 20))
            
            # Countdown label
            self.countdown_label = ctk.CTkLabel(
                main_frame,
                text="⏱️ 15 seconds remaining",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#FF6B6B"
            )
            self.countdown_label.pack(pady=(0, 20))
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(pady=(10, 15))
            
            # Cancel ride button (Red)
            cancel_ride_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Cancel Ride",
                fg_color="#FF4444",
                hover_color="#CC3333",
                width=140,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=self.cancel_ride_from_window
            )
            cancel_ride_btn.pack(side="left", padx=(0, 15))
            
            # Keep ride button (Green)
            keep_ride_btn = ctk.CTkButton(
                buttons_frame,
                text="✅ Keep Ride",
                fg_color="#4CAF50",
                hover_color="#45A049",
                width=140,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=self.keep_ride_from_window
            )
            keep_ride_btn.pack(side="left")
            
            # Start countdown timer
            self.start_countdown_timer()
            
            # Handle dialog close event
            self.cancellation_dialog.protocol("WM_DELETE_WINDOW", self.keep_ride_from_window)
            
        except Exception as e:
            print(f"Error creating cancellation dialog: {e}")
            self.is_cancellation_active = False

    def start_countdown_timer(self):
        """Start the 15-second countdown timer"""
        def countdown_thread():
            try:
                for remaining in range(15, 0, -1):
                    if not self.is_cancellation_active or not self.cancellation_dialog:
                        break
                        
                    # Update countdown display on main thread
                    self.window.after(0, lambda r=remaining: self.update_countdown_display(r))
                    time.sleep(1)
                
                # Auto-close dialog after 15 seconds
                if self.is_cancellation_active and self.cancellation_dialog:
                    self.window.after(0, self.auto_close_cancellation_window)
                    
            except Exception as e:
                print(f"Error in countdown timer: {e}")
        
        # Start countdown in separate thread
        self.cancellation_timer = threading.Thread(target=countdown_thread, daemon=True)
        self.cancellation_timer.start()

    def update_countdown_display(self, remaining):
        """Update the countdown display"""
        try:
            if self.countdown_label and self.cancellation_dialog:
                if remaining > 5:
                    color = "#FF6B6B"  # Red
                    emoji = "⏱️"
                elif remaining > 2:
                    color = "#FFA500"  # Orange
                    emoji = "⚠️"
                else:
                    color = "#FF0000"  # Bright red
                    emoji = "🚨"
                
                self.countdown_label.configure(
                    text=f"{emoji} {remaining} second{'s' if remaining != 1 else ''} remaining",
                    text_color=color
                )
        except Exception as e:
            print(f"Error updating countdown: {e}")

    def auto_close_cancellation_window(self):
        """Auto-close cancellation window after timeout"""
        try:
            if self.cancellation_dialog:
                self.cancellation_dialog.destroy()
                self.cancellation_dialog = None

            self.is_cancellation_active = False

            # *** STORE BOOKING INFO BEFORE CLEARING ***
            if self.current_booking:
                self._last_booking_info = self.current_booking.copy()  # Store booking info
                booking_id = self.current_booking['booking_id']
                
                try:
                    self.booking_history.update_booking_status(booking_id, "In Progress")
                    print(f"✅ Updated booking {booking_id} status to In Progress in history")
                except Exception as e:
                    print(f"❌ Error updating booking status in history: {e}")

                # Show confirmation that the ride is confirmed
                messagebox.showinfo("Ride Confirmed ✅", 
                                f"Your ride has been confirmed!\n"
                                f"Driver is on their way.")

            # Reset current booking AFTER storing info
            self.current_booking = None
            self.show_trip_duration_popup()

        except Exception as e:
            print(f"Error auto-closing cancellation window: {e}")

    def cancel_ride_from_window(self):
        """Cancel ride from the cancellation window"""
        try:
            # Close cancellation dialog
            if self.cancellation_dialog:
                self.cancellation_dialog.destroy()
                self.cancellation_dialog = None

            self.is_cancellation_active = False

            # Cancel the current booking
            if self.current_booking:
                booking_id = self.current_booking['booking_id']

                # *** RELEASE DRIVER BACK TO AVAILABLE AND SAVE TO CSV ***
                released_driver = self.driver_manager.release_driver_to_available(booking_id)

                # *** UPDATE BOOKING STATUS TO CANCELLED IN HISTORY ***
                try:
                    self.booking_history.update_booking_status(booking_id, "Cancelled")
                    print(f"✅ Updated booking {booking_id} status to Cancelled in history")
                except Exception as e:
                    print(f"❌ Error updating booking status in history: {e}")

                if released_driver:
                    messagebox.showinfo("Ride Cancelled ✅", 
                                    f"Your ride (Booking ID: {booking_id}) has been cancelled.\n"
                                    f"Driver {released_driver.driver_name} is now available for other rides.\n\n"
                                    "No charges have been applied.")
                else:
                    messagebox.showwarning("Error ⚠️", "Could not find driver to release.")

                self.current_booking = None
                self.reset_form()
            else:
                messagebox.showwarning("Error ⚠️", "No active booking found to cancel.")

        except Exception as e:
            print(f"Error cancelling ride: {e}")
            messagebox.showerror("Error ❌", "An error occurred while cancelling the ride.")

    def keep_ride_from_window(self):
        """Keep ride from the cancellation window"""
        try:
            # Close cancellation dialog
            if self.cancellation_dialog:
                self.cancellation_dialog.destroy()
                self.cancellation_dialog = None

            self.is_cancellation_active = False

            # *** STORE BOOKING INFO BEFORE CLEARING ***
            if self.current_booking:
                self._last_booking_info = self.current_booking.copy()  # Store booking info
                booking_id = self.current_booking['booking_id']
                

                # *** UPDATE BOOKING STATUS TO IN_PROGRESS IN HISTORY ***
                try:
                    self.booking_history.update_booking_status(booking_id, "In Progress")
                    print(f"✅ Updated booking {booking_id} status to In Progress in history")
                except Exception as e:
                    print(f"❌ Error updating booking status in history: {e}")

                # Show confirmation
                messagebox.showinfo("Ride Confirmed ✅", 
                                f"Great! Your ride has been confirmed.\n"
                                f"The driver is on their way!")

            # Reset current booking AFTER storing info
            self.current_booking = None
            self.show_trip_duration_popup()

        except Exception as e:
            print(f"Error keeping ride: {e}")


    def show_trip_duration_popup(self):
        """Show trip duration popup with countdown timer based on ETA (now minimizable)"""
        try:
            # Calculate ETA for the current booking
            pickup_pos = self.map_widget.get_pickup_position() if self.map_widget else None
            dropoff_pos = self.map_widget.get_dropoff_position() if self.map_widget else None

            if not pickup_pos or not dropoff_pos:
                messagebox.showwarning("Error ⚠️", "Cannot calculate trip duration - missing location data")
                return
        
            # Get the last booking details before they get cleared
            if not hasattr(self, '_last_booking_info') or not self._last_booking_info:
                if self.current_booking:
                    self._last_booking_info = self.current_booking.copy()
                else:
                    messagebox.showwarning("Error ⚠️", "No booking information available")
                    return
        
            booking_info = self._last_booking_info
            
            # Vehicle type mapping
            vehicle_type_mapping = {
                'Car(4 Seater)': 'Car4Seater',
                'Car(6 Seater)': 'Car6Seater', 
                'Mini Van': 'Minivan',
                'Van': 'Van',
                'Motorcycle': 'Motorcycle',
            }
            
            # Get vehicle type from booking info
            vehicle_type = booking_info.get('vehicle_type')
            
            if not vehicle_type:
                print(f"Available keys in booking_info: {list(booking_info.keys())}")
                messagebox.showwarning("Error ⚠️", "Vehicle type information not available")
                return
            
            # Map the vehicle type to the correct format
            mapped_vehicle_type = vehicle_type_mapping.get(vehicle_type, vehicle_type)
            
            # Get the vehicle object
            vehicle = self.get_vehicle_by_type(mapped_vehicle_type)
            
            if not vehicle:
                messagebox.showwarning("Error ⚠️", f"Vehicle information not available for type: {mapped_vehicle_type}")
                return
            
            # Calculate ETA
            eta_info = self.eta_calculator.calculate_eta_for_vehicle(
                pickup_pos[0], pickup_pos[1],
                dropoff_pos[0], dropoff_pos[1],
                vehicle
            )
        
            # Get trip duration in minutes
            trip_duration_minutes = int(eta_info.get('eta_minutes', 15))  # Default to 15 minutes if calculation fails
        
            if trip_duration_minutes <= 0:
                trip_duration_minutes = 1  # Minimum duration
        
            # Create trip duration dialog
            self.trip_dialog = ctk.CTkToplevel(self.window)
            self.trip_dialog.title("🚗 Trip in Progress")
            self.trip_dialog.geometry("500x400")
            self.trip_dialog.transient(self.window)
            
            # Center the dialog
            self.trip_dialog.geometry("+%d+%d" % (
                self.window.winfo_rootx() + 50,
                self.window.winfo_rooty() + 50
            ))
            
            self.trip_dialog_minimized = False
            self.trip_dialog_original_geometry = "500x400"
            
            # Main frame
            main_frame = ctk.CTkFrame(self.trip_dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Header frame
            header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 10))
            
            # Title
            title_label = ctk.CTkLabel(
                header_frame,
                text="🚗 Trip in Progress",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title_label.pack(side="left", pady=(15, 10))
            
            # Minimize/Maximize button
            self.minimize_btn = ctk.CTkButton(
                header_frame,
                text="➖",
                width=30,
                height=30,
                fg_color="#666666",
                hover_color="#555555",
                command=self.toggle_trip_dialog_minimize
            )
            self.minimize_btn.pack(side="right", pady=(15, 10))
            
            # Content frame (this will be hidden/shown when minimizing)
            self.trip_content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            self.trip_content_frame.pack(fill="both", expand=True)
            
            # Trip info (moved to content frame)
            driver_info = booking_info.get('driver', {})
            trip_info = f"Driver: {driver_info.get('driver_name', 'Unknown')}\n"
            trip_info += f"Vehicle: {driver_info.get('vehicle_name', 'Unknown')} ({driver_info.get('plate_no', 'Unknown')})\n"
            trip_info += f"From: {booking_info.get('pickup_location', 'Unknown')}\n"
            trip_info += f"To: {booking_info.get('dropoff_location', 'Unknown')}"
            
            trip_info_label = ctk.CTkLabel(
                self.trip_content_frame,
                text=trip_info,
                font=ctk.CTkFont(size=12),
                justify="left"
            )
            trip_info_label.pack(pady=(0, 20))
            
            # Trip duration countdown (moved to content frame)
            self.trip_countdown_label = ctk.CTkLabel(
                self.trip_content_frame,
                text=f"⏱️ Estimated Duration: {self.eta_calculator.format_eta_time(trip_duration_minutes)}",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#4CAF50"
            )
            self.trip_countdown_label.pack(pady=(0, 10))
            
            # Remaining time label (moved to content frame)
            self.trip_remaining_label = ctk.CTkLabel(
                self.trip_content_frame,
                text=f"🕐 Time Remaining: {self.eta_calculator.format_eta_time(trip_duration_minutes)}",
                font=ctk.CTkFont(size=16),
                text_color="#2196F3"
            )
            self.trip_remaining_label.pack(pady=(0, 20))
            
            # Progress bar (moved to content frame)
            self.trip_progress = ctk.CTkProgressBar(self.trip_content_frame, width=400, height=20)
            self.trip_progress.set(0)
            self.trip_progress.pack(pady=(0, 20))
            
            # ETA info if available (moved to content frame)
            if eta_info.get('arrival_time'):
                arrival_text = self.eta_calculator.format_arrival_time(eta_info['arrival_time'])
                eta_label = ctk.CTkLabel(
                    self.trip_content_frame,
                    text=f"🎯 Expected Arrival: {arrival_text}",
                    font=ctk.CTkFont(size=14),
                    text_color="#666666"
                )
                eta_label.pack(pady=(0, 15))
            
            # Complete trip button (initially disabled) (moved to content frame)
            self.complete_trip_btn = ctk.CTkButton(
                self.trip_content_frame,
                text="🏁 Complete Trip",
                fg_color="#4CAF50",
                hover_color="#45A049",
                width=200,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=self.complete_trip_early,
                state="disabled"
            )
            self.complete_trip_btn.pack(pady=(10, 15))
            
            # Info text (moved to content frame)
            info_text = "Trip will automatically complete when timer reaches zero.\nYou can manually complete it in the last 2 minutes."
            info_label = ctk.CTkLabel(
                self.trip_content_frame,
                text=info_text,
                font=ctk.CTkFont(size=10),
                text_color="#666666",
                justify="center"
            )
            info_label.pack(pady=(0, 10))
            
            # Change dialog close behavior to allow minimizing
            self.trip_dialog.protocol("WM_DELETE_WINDOW", self.minimize_trip_dialog)
            
            # Start trip countdown
            self.start_trip_countdown(trip_duration_minutes)
        
        except Exception as e:
            print(f"Error showing trip duration popup: {e}")
            messagebox.showerror("Error ❌", f"Failed to show trip duration popup: {str(e)}")

    def start_trip_countdown(self, total_minutes):
        """Start the trip countdown timer"""
        def trip_countdown_thread():
            try:
                total_seconds = int(total_minutes * 60)
            
                for remaining_seconds in range(total_seconds, 0, -1):
                    if not hasattr(self, 'trip_dialog') or not self.trip_dialog:
                        break
                
                    remaining_minutes = remaining_seconds / 60
                    progress = (total_seconds - remaining_seconds) / total_seconds
                
                    # Update UI on main thread
                    self.window.after(0, lambda rm=remaining_minutes, p=progress, rs=remaining_seconds: 
                                    self.update_trip_countdown_display(rm, p, rs, total_minutes))
                
                    time.sleep(1)
            
                # Auto-complete trip when timer reaches zero
                if hasattr(self, 'trip_dialog') and self.trip_dialog:
                    self.window.after(0, self.auto_complete_trip)
                
            except Exception as e:
                print(f"Error in trip countdown timer: {e}")
    
        # Start countdown in separate thread
        self.trip_countdown_timer = threading.Thread(target=trip_countdown_thread, daemon=True)
        self.trip_countdown_timer.start()



    def toggle_trip_dialog_minimize(self):
        """Toggle minimize/maximize state of trip dialog"""
        try:
            if not hasattr(self, 'trip_dialog') or not self.trip_dialog:
                return
                
            if self.trip_dialog_minimized:
                # Maximize
                self.trip_dialog.geometry(self.trip_dialog_original_geometry)
                self.trip_content_frame.pack(fill="both", expand=True)
                self.minimize_btn.configure(text="➖")
                self.trip_dialog_minimized = False
            else:
                # Minimize
                self.trip_dialog_original_geometry = self.trip_dialog.geometry()
                self.trip_dialog.geometry("500x80")  # Only show header
                self.trip_content_frame.pack_forget()
                self.minimize_btn.configure(text="⬜")
                self.trip_dialog_minimized = True
                
        except Exception as e:
            print(f"Error toggling trip dialog minimize: {e}")

    def minimize_trip_dialog(self):
        """Minimize trip dialog instead of closing"""
        try:
            if hasattr(self, 'trip_dialog') and self.trip_dialog:
                if not self.trip_dialog_minimized:
                    self.toggle_trip_dialog_minimize()
        except Exception as e:
            print(f"Error minimizing trip dialog: {e}")

    def restore_trip_dialog(self):
        """Restore trip dialog from minimized state"""
        try:
            if hasattr(self, 'trip_dialog') and self.trip_dialog and self.trip_dialog_minimized:
                self.toggle_trip_dialog_minimize()
        except Exception as e:
            print(f"Error restoring trip dialog: {e}")


    def show_booking_confirmation(self, booking_details):
        """Original booking confirmation method (kept for compatibility)"""
        self.show_booking_confirmation_with_cancellation(booking_details)



    def update_trip_countdown_display(self, remaining_minutes, progress, remaining_seconds, total_minutes):
        """Update the trip countdown display"""
        try:
            if not hasattr(self, 'trip_dialog') or not self.trip_dialog:
                return
        
            # Update remaining time
            remaining_time_text = self.eta_calculator.format_eta_time(remaining_minutes)
            self.trip_remaining_label.configure(text=f"🕐 Time Remaining: {remaining_time_text}")
        
            # Update progress bar
            self.trip_progress.set(progress)
        
            # Enable complete button in last 2 minutes
            if remaining_minutes <= 2:
                self.complete_trip_btn.configure(state="normal")
                if remaining_minutes <= 0.5:  # Last 30 seconds
                    self.trip_remaining_label.configure(text_color="#FF0000")
                    self.complete_trip_btn.configure(fg_color="#FF4444", hover_color="#CC3333")
        
            # Update colors based on remaining time
            if remaining_minutes > 5:
                color = "#4CAF50"  # Green
            elif remaining_minutes > 2:
                color = "#FF9800"  # Orange
            else:
                color = "#F44336"  # Red
        
            self.trip_countdown_label.configure(text_color=color)
        
        except Exception as e:
            print(f"Error updating trip countdown display: {e}")

    def complete_trip_early(self):
        """Handle early trip completion"""
        try:
            result = messagebox.askyesno(
                "Complete Trip Early? 🏁", 
                "Are you sure you want to complete the trip now?\n\n"
                "This will end the trip and mark it as completed."
            )
        
            if result:
                self.complete_trip()
            
        except Exception as e:
            print(f"Error completing trip early: {e}")

    def auto_complete_trip(self):
        """Auto-complete trip when timer reaches zero"""
        try:
            if hasattr(self, 'trip_dialog') and self.trip_dialog:
                # Show completion message
                messagebox.showinfo(
                    "Trip Completed! 🎉", 
                    "Your trip has been completed!\n\n"
                    "Thank you for using Go-Do!"
                )
            
                self.complete_trip()
            
        except Exception as e:
            print(f"Error auto-completing trip: {e}")

    def complete_trip(self):
        """Complete the current trip"""
        try:
            # Close trip dialog
            if hasattr(self, 'trip_dialog') and self.trip_dialog:
                self.trip_dialog.destroy()
                self.trip_dialog = None
        
            # *** NOW RELEASE THE DRIVER WHEN TRIP IS ACTUALLY COMPLETED ***
            if hasattr(self, '_last_booking_info') and self._last_booking_info:
                booking_id = self._last_booking_info['booking_id']
                
                # *** RELEASE DRIVER BACK TO AVAILABLE STATUS ***
                released_driver = self.driver_manager.release_driver_to_available(booking_id)
                
                if released_driver:
                    print(f"✅ Released driver {released_driver.driver_name} back to available status")
            
                # Update booking history to completed
                try:
                    self.booking_history.update_booking_status(booking_id, "Completed")
                    print(f"✅ Updated booking {booking_id} status to Completed in history")
                except Exception as e:
                    print(f"❌ Error updating booking status in history: {e}")
        
            # Clear stored booking info
            self._last_booking_info = None
            self.current_booking = None
        
            # Reset form for next booking
            self.reset_form()
        
            print("✅ Trip completed successfully")
        
        except Exception as e:
            print(f"Error completing trip: {e}")
            messagebox.showerror("Error ❌", "An error occurred while completing the trip")

    def cancel_current_booking(self):
        """Cancel the current booking and release the driver (original method)"""
        if self.current_booking:
            booking_id = self.current_booking['booking_id']
            driver_name = self.current_booking['driver']['driver_name']
            
            # Release the driver
            self.driver_manager.release_driver(booking_id)
            
            messagebox.showinfo("Booking Cancelled ❌", 
                              f"Booking {booking_id} has been cancelled.\n"
                              f"Driver {driver_name} is now available for other rides.")
            
            self.current_booking = None
            self.reset_form()
        else:
            messagebox.showwarning("No Active Booking ⚠️", "No active booking to cancel.")

    def show_eta_comparison(self):
        """Show ETA comparison for all available vehicle types"""
        pickup_pos = self.map_widget.get_pickup_position() if self.map_widget else None
        dropoff_pos = self.map_widget.get_dropoff_position() if self.map_widget else None
        
        if not pickup_pos or not dropoff_pos:
            messagebox.showwarning("Missing Locations ⚠️", 
                                 "Please select both pickup and dropoff locations first.")
            return
        
        vehicle_types = ["Car4Seater", "Car6Seater", "Minivan", "Van", "Motorcycle"]
        comparison_text = "🚗 ETA Comparison:\n\n"
        
        for vehicle_type in vehicle_types:
            vehicle = self.get_vehicle_by_type(vehicle_type)
            if vehicle:
                eta_info = ETACalculator.calculate_eta_for_vehicle(
                    pickup_pos[0], pickup_pos[1],
                    dropoff_pos[0], dropoff_pos[1],
                    vehicle
                )
                
                comparison_text += f"🚙 {vehicle_type}:\n"
                comparison_text += f"   ⏱️ {eta_info['eta_formatted']}\n"
                comparison_text += f"   🏃 Speed: {vehicle.average_speed} km/h\n"
                
                comparison_text += "\n"
        
        messagebox.showinfo("ETA Comparison 📊", comparison_text)
    
    def get_distance_and_eta_info(lat1, lng1, lat2, lng2, vehicle_type=""):
        from Modules.vehicle import Car4Seater, Car6Seater, Minivan, Van, Motorcycle
    
        # Calculate distance
        distance_km = DistanceCalculator.calculate_distance_km(lat1, lng1, lat2, lng2)
        distance_formatted = DistanceCalculator.format_distance(lat1, lng1, lat2, lng2)
    
        # Get vehicle and calculate ETA
        vehicle_map = {
            "Car4Seater": Car4Seater("Sample Car 4"),
            "Car6Seater": Car6Seater("Sample Car 6"),
            "Minivan": Minivan("Sample Minivan"),
            "Van": Van("Sample Van"),
            "Motorcycle": Motorcycle("Sample Motorcycle")
        }
    
        vehicle = vehicle_map.get(vehicle_type)
        eta_info = ETACalculator.calculate_eta_for_vehicle(lat1, lng1, lat2, lng2, vehicle)
    
        return {
            "distance_km": distance_km,
            "distance_formatted": distance_formatted,
            "eta_minutes": eta_info['eta_minutes'],
            "eta_formatted": eta_info['eta_formatted'],
            "arrival_time": eta_info.get('arrival_time'),
            "vehicle_speed": vehicle.average_speed,
            "summary": f"{distance_formatted} • {eta_info['eta_formatted']}"
        }

    def show_driver_availability(self):
        """Show current driver availability"""
        availability_info = "📊 Driver Availability Status:\n\n"
        
        vehicle_types = self.driver_manager.get_available_vehicle_types()
        for vehicle_type in vehicle_types:
            total, available = self.driver_manager.get_driver_count_by_type(vehicle_type)
            status_emoji = "🟢" if available > 0 else "🔴"
            availability_info += f"{status_emoji} {vehicle_type}:\n"
            availability_info += f"   Available: {available}/{total}\n\n"
        
        messagebox.showinfo("Driver Availability 📋", availability_info)

    def reset_all_drivers_status(self):
        """Reset all drivers to available status (for testing/admin)"""
        result = messagebox.askyesno("Reset All Drivers ⚠️", 
                                   "This will reset all drivers to available status.\n"
                                   "Are you sure you want to continue?")
        if result:
            self.driver_manager.reset_all_drivers()
            self.current_booking = None
            messagebox.showinfo("Reset Complete ✅", 
                              "All drivers have been reset to available status.")

    def reset_form(self):
        """Reset the form to initial state"""
        self.ui_manager.reset_entries()
    
        # Clear driver information
        self.ui_manager.right_panel.update_driver_info(None)
    
        # Clear map markers
        if self.map_widget:
            self.map_widget._clear_all()
    
    def show_location_confirmation_dialog(self, lat, lng, address):
        """Show custom confirmation dialog with colored buttons"""
        try:
            dialog = ctk.CTkToplevel(self.window)
            dialog.title("📍 Set Location")
            dialog.geometry("400x250")
            dialog.transient(self.window)
            dialog.grab_set()
            
            # Center the dialog
            dialog.geometry("+%d+%d" % (
                self.window.winfo_rootx() + 50,
                self.window.winfo_rooty() + 50
            ))
            
            # Main frame
            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title_label = ctk.CTkLabel(
                main_frame,
                text="Set this location?",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=(10, 15))
            
            # Address
            address_label = ctk.CTkLabel(
                main_frame,
                text=f"📍 {address[:60]}{'...' if len(address) > 60 else ''}",
                font=ctk.CTkFont(size=12),
                wraplength=350
            )
            address_label.pack(pady=(0, 10))
            
            # Coordinates
            coord_label = ctk.CTkLabel(
                main_frame,
                text=f"🌐 {lat:.6f}, {lng:.6f}",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            coord_label.pack(pady=(0, 20))
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=(10, 0))
            
            # Pickup button (Green)
            pickup_btn = ctk.CTkButton(
                buttons_frame,
                text="🚗 Pickup",
                fg_color="#4CAF50",
                hover_color="#45A049",
                width=100,
                height=40,
                command=lambda: self.handle_dialog_choice(dialog, lat, lng, address, "pickup")
            )
            pickup_btn.pack(side="left", padx=(0, 10))
            
            # Dropoff button (Red)
            dropoff_btn = ctk.CTkButton(
                buttons_frame,
                text="🏁 Dropoff",
                fg_color="#F44336",
                hover_color="#D32F2F", 
                width=100,
                height=40,
                command=lambda: self.handle_dialog_choice(dialog, lat, lng, address, "dropoff")
            )
            dropoff_btn.pack(side="left", padx=(0, 10))
            
            # Cancel button
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ Cancel",
                fg_color="gray",
                hover_color="darkgray",
                width=80,
                height=40,
                command=dialog.destroy
            )
            cancel_btn.pack(side="right")
            
        except Exception as e:
            print(f"Error creating location dialog: {e}")
    
    def handle_dialog_choice(self, dialog, lat, lng, address, location_type):
        """Handle dialog button choice"""
        try:
            dialog.destroy()
            self.set_clicked_location(lat, lng, address, location_type)
        except Exception as e:
            print(f"Error handling dialog choice: {e}")
    
    def set_clicked_location(self, lat, lng, address, location_type):
        """Set the clicked location as pickup or dropoff"""
        try:
            shortened_address = address[:50] + "..." if len(address) > 50 else address
        
            if location_type == "pickup":
                if self.map_widget:
                    self.map_widget.set_custom_pickup_location(lat, lng, address)
                self.ui_manager.set_pickup_location(lat, lng, shortened_address)
            else:
                if self.map_widget:
                    self.map_widget.set_custom_dropoff_location(lat, lng, address)
                self.ui_manager.set_dropoff_location(lat, lng, shortened_address)
        
            # Update distance display after setting locations
            self.update_distance_display()
        
        except Exception as e:
            print(f"Error setting clicked location: {e}")
    
    def update_distance_display(self):
        """Update the distance display with ETA information"""
        try:
            if not self.map_widget:
                return
            
            pickup_pos = self.map_widget.get_pickup_position()
            dropoff_pos = self.map_widget.get_dropoff_position()
            
            if pickup_pos and dropoff_pos:
                # Calculate distance
                distance_text = DistanceCalculator.format_distance(
                    pickup_pos[0], pickup_pos[1], dropoff_pos[0], dropoff_pos[1]
                )
                
                # Calculate ETA for selected vehicle if available
                selected_vehicle = self.ui_manager.get_selected_vehicle()
                eta_text = ""
                
                if selected_vehicle:
                    # Get vehicle object (assuming you have a method to get vehicle by type)
                    vehicle = self.get_vehicle_by_type(selected_vehicle)
                    if vehicle:
                        eta_info = ETACalculator.calculate_eta_for_vehicle(
                            pickup_pos[0], pickup_pos[1], 
                            dropoff_pos[0], dropoff_pos[1], 
                            vehicle
                        )
                        eta_text = f"\n⏱️ ETA: {eta_info['eta_formatted']}"
                        
                        
                        # Show arrival time
                        if eta_info.get("arrival_time"):
                            arrival_text = ETACalculator.format_arrival_time(eta_info["arrival_time"])
                            eta_text += f"\n🎯 Arrival: {arrival_text}"
                
                # Update display with distance and ETA
                display_text = f"📏 Distance: {distance_text}{eta_text}"
                self.ui_manager.left_panel.distance_label.configure(
                    text=display_text, 
                    text_color="green"
                )
            else:
                self.ui_manager.left_panel.distance_label.configure(
                    text="📍 Select pickup and dropoff locations", 
                    text_color="#666666"
                )
                
        except Exception as e:
            print(f"Error updating distance display: {e}")
            self.ui_manager.left_panel.distance_label.configure(
                text="❌ Error calculating distance", 
                text_color="red"
            )

    def get_vehicle_by_type(self, vehicle_type):
        
        from Modules.vehicle import Car4Seater, Car6Seater, Minivan, Van, Motorcycle
        
        vehicle_map = {
            "Car4Seater": Car4Seater("Sample Car 4"),
            "Car6Seater": Car6Seater("Sample Car 6"),
            "Minivan": Minivan("Sample Minivan"),
            "Van": Van("Sample Van"),
            "Motorcycle": Motorcycle("Sample Motorcycle")
        }
        
        return vehicle_map.get(vehicle_type)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        current_state = self.window.attributes('-fullscreen')
        self.window.attributes('-fullscreen', not current_state)
        self.window.after(200, self.ui_manager.resize_components)
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.window.attributes('-fullscreen', False)
        self.window.after(200, self.ui_manager.resize_components)
    
    def show_controls_info(self):
        """Show controls information"""
        controls_message = """🎮 Controls & Features:

🔧 Fullscreen Controls:
• F11 - Toggle fullscreen
• Alt+Enter - Toggle fullscreen  
• Escape - Exit fullscreen

🗺️ Map Controls:
• Click on map to set pickup/dropoff

🚗 Driver Management:
• Automatic driver assignment
• Real-time availability checking
• Complete driver information

🎯 Booking Features:
• Distance calculation
• Fare estimation
• Payment options
• Booking confirmation with driver details
• 15-second cancellation window after booking
• Cancel current booking"""
        
        messagebox.showinfo("🎮 Controls & Features", controls_message)

    def create_admin_menu(self):
        """Create admin menu buttons in the header (optional)"""
        # Add admin buttons to the header frame if needed
        # This could include buttons for:
        # - View driver availability
        # - Cancel current booking  
        # - Reset all drivers
        # - View booking history
        pass

    def run(self):
        """Start the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = MapWithDistanceRideBookingApp()
    app.run()