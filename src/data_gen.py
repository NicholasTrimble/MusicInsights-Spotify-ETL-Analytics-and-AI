import os
import csv
import random
from datetime import datetime
from faker import Faker

# I used Faker to generate fake data

fake = Faker()

# Make sure folder exists
os.makedirs("data/raw", exist_ok=True)

#Now i need to generate users

def generate_users(n=10):
    users = []
    for i in range(1, n + 1):
        user_id = i
        email = fake.email()
        signup_date = str(datetime.now().date())
        country = fake.country()

        users.append([user_id, email, signup_date, country])
    return users

#This part will be to generate my products

def generate_products(n=5):
    products = []
    categories = ["books", "electronics", "clothing"]
    for i in range(1, n + 1):
        product_id = i
        name = f"Product {i}"
        category = random.choice(categories)
        price = round(random.uniform(5, 100), 2)
        products.append([product_id, name, category, price])
    return products

# Now i will generate the orders

def generate_orders(users, products, n=20):
    orders = []
    for i in range(1, n + 1):
        user = random.choice(users)
        product = random.choice(products)
        order_id = i
        user_id = user[0]
        product_id = product[0]
        quantity = random.randint(1, 5)
        price = product[3]
        order_datetime = str(datetime.now())
        orders.append([order_id, user_id, product_id, quantity, price, order_datetime])
    return orders

#this will be to set up the csv writer


def write_csv(filename, rows, header):
    with open(f"data/raw/{filename}", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

# Now i will use my main function to run the pipeline

if __name__ == "__main__":
    users = generate_users(50)
    products = generate_products(10)
    orders = generate_orders(users, products, 100)

    write_csv("users.csv", users, ["user_id", "email", "signup_date", "country"])
    write_csv("products.csv", products, ["product_id", "name", "category", "price"])
    write_csv("orders.csv", orders, ["order_id", "user_id", "product_id", "quantity", "price", "order_datetime"])
