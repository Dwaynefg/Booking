from booking import Booking
import csv
import os

class BookingManager:
    def __init__(self, filename='bookings.csv'):
        self.filename = filename
        self.bookings = self.load_bookings()

    def add_booking(self, booking):
        self.bookings.append(booking)
        self.save_bookings()

    def cancel_booking(self, booking_id, user=None, is_admin=False):
        if is_admin:
            self.bookings = [b for b in self.bookings if str(b.booking_id) != str(booking_id)]
        else:
            self.bookings = [b for b in self.bookings if str(b.booking_id) != str(booking_id) or b.user != user]
        self.save_bookings()

    def save_bookings(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['booking_id', 'user', 'vehicle_type', 'start', 'end', 'distance', 'cost'])
            for b in self.bookings:
                writer.writerow([b.booking_id, b.user, b.vehicle_type, b.start, b.end, b.distance, b.cost])

    def load_bookings(self):
        bookings = []
        if not os.path.exists(self.filename):
            return bookings
        with open(self.filename, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                booking = Booking(
                    booking_id=row['booking_id'],
                    user=row['user'],
                    vehicle_type=row['vehicle_type'],
                    start=row['start'],
                    end=row['end'],
                    distance=float(row['distance']),
                    cost=float(row['cost'])
                )
                bookings.append(booking)
        return bookings

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

USERS = [
    User('admin', 'adminpass', 'Admin'),
    User('user', 'userpass', 'User')
]
