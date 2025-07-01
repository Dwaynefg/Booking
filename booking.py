from datetime import datetime

class Booking:
    def __init__(
        self, bookingID, userName, driverName, vehicle, pickup, drop_off,
        distance_km, paymentMethod, status="Pending", bookingDate=None
    ):
        self.bookingID = bookingID
        self.bookingDate = bookingDate or datetime.now().strftime("%Y-%m-%d")
        self.userName = userName
        self.driverName = driverName
        self.vehicle = vehicle
        self.pickup = pickup
        self.drop_off = drop_off
        self.distance_km = float(distance_km)
        self.paymentMethod = paymentMethod
        self.status = status

        # Calculating the cost
        self.base_cost, self.tax = self.vehicle.calculate_cost_with_tax(self.distance_km)
        self.totalCost = round(self.base_cost + self.tax, 2)

    def to_dict(self):
        return {
            "bookingID": self.bookingID,
            "bookingDate": self.bookingDate,
            "userName": self.userName,
            "driverName": self.driverName,
            "vehicleType": self.vehicle.__class__.__name__,
            "vehicleName": self.vehicle.name,
            "pickup": self.pickup,
            "drop-off": self.drop_off,
            "distance_km": f"{self.distance_km:.1f}",
            # "duration_min" removed
            "cost_per_mile": f"{self.vehicle.cost_per_mile:.2f}",
            "tax": f"{self.tax:.2f}",
            "totalCost": f"{self.totalCost:.2f}",
            "paymentMethod": self.paymentMethod,
            "status": self.status
        }

    def __str__(self):
        return (f"BookingID: {self.bookingID}, Date: {self.bookingDate}, User: {self.userName}, "
                f"Driver: {self.driverName}, Vehicle: {self.vehicle.category} {self.vehicle.name}, "
                f"From: {self.pickup} To: {self.drop_off}, Distance: {self.distance_km} km, "
                # "Duration" removed from the string
                f"Cost: ${self.totalCost:.2f}, Payment: {self.paymentMethod}, Status: {self.status}")
