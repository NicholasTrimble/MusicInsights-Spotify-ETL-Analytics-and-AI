import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "sqlite:///data/warehouse.db"

def compute_kpis():
    engine = create_engine(DB_PATH)
    orders = pd.read_sql_table("orders", engine)

    total_revenue = orders["total_price"].sum()
    total_orders = orders["order_id"].nunique()
    avg_order_value = total_revenue / total_orders
    unique_users = orders["user_id"].nunique()

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "unique_users": unique_users,

    }

if __name__ == "__main__":
    print(compute_kpis())