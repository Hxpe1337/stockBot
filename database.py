import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks
        (product TEXT, account TEXT)
        """)

    def insert_product(self, product):
        self.cursor.execute("INSERT INTO stocks (product) VALUES (?)", (product,))
        self.conn.commit()


    def delete_account(self, product, account):
        self.cursor.execute("DELETE FROM stocks WHERE product = ? AND account = ?", (product, account))
        self.conn.commit()

    def clear_product(self, product):
        self.cursor.execute("DELETE FROM stocks WHERE product=?", (product,))
        self.cursor.execute("DELETE FROM stocks WHERE product=? AND account IS NULL", (product,))
        self.conn.commit()


    def add_account(self, product, account):
        self.cursor.execute("INSERT INTO stocks VALUES (?, ?)", (product, account))
        self.conn.commit()


    def get_stock(self, product):
        self.cursor.execute("SELECT COUNT(account) FROM stocks WHERE product = ?", (product,))
        return self.cursor.fetchone()
    def get_all_accounts(self, product):
        self.cursor.execute("SELECT account FROM stocks WHERE product=?", (product,))
        return self.cursor.fetchall()

    def get_all_stocks(self):
        self.cursor.execute("SELECT product, COUNT(account) FROM stocks GROUP BY product")
        return self.cursor.fetchall()

    def get_random_account(self, product):
        self.cursor.execute("SELECT account FROM stocks WHERE product = ? AND account IS NOT NULL ORDER BY RANDOM() LIMIT 1", (product,))
        return self.cursor.fetchone()

