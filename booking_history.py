import csv
from booking import Booking
from vehicle import *

BOOKING_CSV_FILE = "bookings.csv"
print("booking_history loaded")
print(dir())
def save_bookings_to_csv(bookings):
    with open(BOOKING_CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "bookingID", "bookingDate", "userName", "driverName",
            "vehicleType", "vehicleName", "pickup", "drop-off",
            "distance_km", "duration_min", "cost_per_mile", "tax",
            "totalCost", "paymentMethod", "status"
        ])
        for booking in bookings:
            d = booking.to_dict()
            writer.writerow([
                d["bookingID"],
                d["bookingDate"],
                d["userName"],
                d["driverName"],
                d["vehicleType"],
                d["vehicleName"],
                d["pickup"],
                d["drop-off"],
                d["distance_km"],
                d["duration_min"],
                d["cost_per_mile"],
                d["tax"],
                d["totalCost"],
                d["paymentMethod"],
                d["status"],
            ])

def load_bookings_from_csv():
    bookings = []
    try:
        with open(BOOKING_CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for r in reader:
                vehicle_type = r["vehicleType"]
                vehicle_name = r["vehicleName"]
                cost_per_mile = float(r["cost_per_mile"])

                vehicle_class_map = {
                    "Car": Car4Seater,  # Adjust based on name
                    "Van": Van,
                    "Minivan": Minivan,
                    "Bike": Bike,
                    "Motorcycle": Motorcycle,
                }
                vehicle_cls = vehicle_class_map.get(vehicle_type, Vehicle)
                vehicle = vehicle_cls(vehicle_name, cost_per_mile)

                booking = Booking(
                    bookingID=r["bookingID"],
                    bookingDate=r["bookingDate"],
                    userName=r["userName"],
                    driverName=r["driverName"],
                    vehicle=vehicle,
                    pickup=r["pickup"],
                    drop_off=r["drop-off"],
                    distance_km=float(r["distance_km"]),
                    duration_min=int(r["duration_min"]),
                    paymentMethod=r["paymentMethod"],
                    status=r["status"]
                )
                bookings.append(booking)
    except FileNotFoundError:
        pass
    return bookings

