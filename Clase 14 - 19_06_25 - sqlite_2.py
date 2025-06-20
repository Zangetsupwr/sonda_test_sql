import sqlite3
import random
from datetime import datetime
from faker import Faker

def populate_database(db_path: str = "mi_base.db", num_users: int = 100, num_orders: int = 100) -> dict:
    """
    Populate the SQLite database with random test data for 'usuarios' and 'ordenes' tables.

    Parameters:
        db_path (str): Path to the SQLite database file.
        num_users (int): Number of users to generate and insert into the 'usuarios' table.
        num_orders (int): Number of orders to generate and insert into the 'ordenes' table.

    Returns:
        dict: A dictionary with the count of inserted users and orders.
              Example: {"users_inserted": 100, "orders_inserted": 100}
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    fake = Faker()

    # Store user IDs to assign them to orders.
    user_ids = []

    # Insert random users into the 'usuarios' table.
    for _ in range(num_users):
        name = fake.name()
        email = fake.unique.email()
        registration_date = fake.date_between(start_date="-2y", end_date="today").isoformat()

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, fecha_registro) VALUES (?, ?, ?)",
            (name, email, registration_date)
        )

    # Retrieve user IDs after insertion.
    cursor.execute("SELECT id FROM usuarios ORDER BY id DESC LIMIT ?", (num_users,))
    user_ids = [row[0] for row in cursor.fetchall()]

    # Sample product list.
    product_list = [
        "Mechanical Keyboard", "Gaming Mouse", "27'' Monitor", "Laptop", "Cooling Pad",
        "Headphones", "Webcam", "Ergonomic Chair", "USB-C Hub", "Microphone"
    ]

    # Insert random orders into the 'ordenes' table.
    for _ in range(num_orders):
        user_id = random.choice(user_ids)
        product = random.choice(product_list)
        amount = round(random.uniform(30, 1500), 2)
        order_date = fake.date_between(start_date="-1y", end_date="today").isoformat()

        cursor.execute(
            "INSERT INTO ordenes (usuario_id, producto, monto, fecha) VALUES (?, ?, ?, ?)",
            (user_id, product, amount, order_date)
        )

    conn.commit()
    conn.close()

    return {
        "users_inserted": num_users,
        "orders_inserted": num_orders
    }

# Run the script if it's executed directly.
if __name__ == "__main__":
    # You can change these values as needed.
    db_file = "mi_base.db"
    result = populate_database(db_path=db_file, num_users=100, num_orders=100)

    print(f"Inserted {result['users_inserted']} users and {result['orders_inserted']} orders into '{db_file}'.")