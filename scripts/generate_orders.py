import csv
import os
import random
from datetime import datetime, timedelta

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune"]
RESTAURANTS = [
    "Spice Hub", "Curry Palace", "Tandoori House", "Pizza Planet",
    "Burger Barn", "Noodle Nation"
]
PAYMENT_METHODS = ["UPI", "CARD", "COD", "NET_BANKING"]
CUISINES = ["Indian", "Chinese", "Italian", "Fast Food", "North Indian"]

def random_datetime_in_last_n_days(n=30):
    now = datetime.now()
    delta = timedelta(days=random.randint(0, n), hours=random.randint(0, 23),
                      minutes=random.randint(0, 59), seconds=random.randint(0, 59))
    return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

def generate_order(order_id: int) -> dict:
    city = random.choice(CITIES)
    restaurant = random.choice(RESTAURANTS)
    base_amount = random.choice([150, 200, 250, 300, 350, 400, 500])
    quantity = random.randint(1, 5)
    order_value = base_amount * quantity
    discount = random.choice([0, 10, 20, 30, 50])
    final_amount = max(order_value - discount, 50)

    return {
        "order_id": order_id,
        "user_id": random.randint(1000, 9999),
        "order_timestamp": random_datetime_in_last_n_days(30),
        "city": city,
        "restaurant_name": restaurant,
        "cuisine": random.choice(CUISINES),
        "payment_method": random.choice(PAYMENT_METHODS),
        "quantity": quantity,
        "order_value": order_value,
        "discount": discount,
        "final_amount": final_amount,
        "delivery_rating": random.randint(1, 5)
    }

def main(num_orders: int = 10000):
    # Ensure data/raw exists
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    output_file = os.path.join(raw_dir, "food_orders.csv")

    fieldnames = [
        "order_id", "user_id", "order_timestamp", "city", "restaurant_name",
        "cuisine", "payment_method", "quantity", "order_value",
        "discount", "final_amount", "delivery_rating"
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, num_orders + 1):
            order = generate_order(i)
            writer.writerow(order)

    print(f"Generated {num_orders} orders at: {output_file}")

if __name__ == "__main__":
    main()
