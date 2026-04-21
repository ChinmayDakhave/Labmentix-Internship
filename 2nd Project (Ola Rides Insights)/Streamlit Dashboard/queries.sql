-- Q1: All successful bookings
SELECT * FROM rides WHERE Booking_Status = 'Success';

-- Q2: Average ride distance per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS avg_distance
FROM rides GROUP BY Vehicle_Type;

-- Q3: Total cancelled rides by customers
SELECT COUNT(*) AS customer_cancellations
FROM rides WHERE Booking_Status = 'Canceled by Customer';

-- Q4: Top 5 customers by number of rides booked
SELECT Customer_ID, COUNT(*) AS total_rides
FROM rides GROUP BY Customer_ID
ORDER BY total_rides DESC LIMIT 5;

-- Q5: Rides cancelled by drivers due to personal/car issues
SELECT COUNT(*) AS driver_cancellations
FROM rides WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Q6: Max and min driver ratings for Prime Sedan
SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating
FROM rides WHERE Vehicle_Type = 'Prime Sedan';

-- Q7: All rides paid by UPI
SELECT * FROM rides WHERE Payment_Method = 'UPI';

-- Q8: Average customer rating per vehicle type
SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS avg_customer_rating
FROM rides GROUP BY Vehicle_Type;

-- Q9: Total booking value of successful rides
SELECT SUM(Booking_Value) AS total_revenue
FROM rides WHERE Booking_Status = 'Success';

-- Q10: All incomplete rides with reason
SELECT Booking_ID, Customer_ID, Vehicle_Type, Incomplete_Rides_Reason
FROM rides WHERE Incomplete_Rides = 'Yes';