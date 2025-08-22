import pandas as pd
import sqlite3


class SqliteConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            print("Connected to SQLite database")
        except sqlite3.Error as e:
            print(e)

    def close(self):
        if self.connection:
            self.connection.close()
            print("SQLite connection closed")


def main():
    """
    1. connect to the SQLite3 database provided
    2. extract the total quantities of each item bought per customer aged 18-35.
        - For each customer, get the sum of each item
        - Items with no purchase (total quantity=0) should be omitted from the final
        list
        - No decimal points allowed (The company doesn’t sell half of an item ;) )
    Challenge: Provide 2 solutions, one using purely SQL, the other using Pandas
    3. store the query to a CSV file, delimiter should be the semicolon character (';')
    """

    conn = SqliteConnection("sqlite/S30 ETL Assignment.db")
    try:
        conn.connect()
        df_customers = pd.read_sql_query("SELECT * FROM customers", conn.connection)
        df_sales = pd.read_sql_query("SELECT * FROM sales", conn.connection)
        df_orders = pd.read_sql_query("SELECT * FROM orders", conn.connection)
        df_items = pd.read_sql_query("SELECT * FROM items", conn.connection)
        df = df_customers.merge(df_sales, on="customer_id", how="left")
        df = df.merge(df_orders, on="sales_id", how="left")
        df = df.merge(df_items, on="item_id", how="left")
        df = (
            df.groupby(["customer_id", "age", "item_name"])
            .agg({"quantity": "sum"})
            .reset_index()
        )
        df = df[df["quantity"] > 0]
        df = df[df["age"] >= 18]
        df = df[df["age"] <= 35]
        df["quantity"] = df["quantity"].astype(int)
        df = df.rename(columns={"item_name": "item"})
        df = df.reset_index(drop=True)

        df.to_csv("output/output.csv", sep=";", index=False)

        print(df)
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
