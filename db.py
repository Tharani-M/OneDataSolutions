from pydantic import BaseModel
from typing import Optional
import  psycopg2 

class productDataModel(BaseModel):
    name: str
    catogory : Optional[str] = "General"
    price: Optional[float] = 0.0
    quantity: Optional[int] =1
    supplier : Optional[str] = None
    created_At: Optional[str] = None
    prod_id: Optional[int] = None

class supplierDataModel(BaseModel):
    supplier_name: Optional[str] = "General Supplier"
    contact_info: Optional[str] = "Not Available"

class productData:
    def __init__(self):
        self.connection = None
        self.connect()
        # self.pd = productDataModel(name="",catogory="", price=0.0, quantity=0,supplier="")
        # self.sd = supplierDataModel(supplier_name="", contact_info="")
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host = "localhost",database = "mydatabase",user = "postgres",password = 123,port = "5432")
            
            print("Connected to the database")
            cursor = self.connection.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS products(
                           prod_id SERIAL PRIMARY KEY,
                           name TEXT NOT NULL,
                           price Float NOT NULL,
                           quantity INTEGER NOT NULL,
                           created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS suppliers(
                           supplier_name TEXT NOT NULL,
                           contact_info TEXT NOT NULL)""")
            self.connection.commit()
            # cursor.close()
        except Exception as e:
            print("Error connecting to the database:", e)

    def addItem(self, pd: productDataModel):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                           INSERT INTO products (name, price, quantity, created_At)
                           VALUES (%s, %s, %s, %s)""",
                           (pd.name, pd.price, pd.quantity, pd.created_At))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error adding item to the database:", e)
            return False    
    
    def updateItem(self,pd:productDataModel):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                           UPDATE products
                           SET name = %s, price = %s, quantity = %s, created_At = %s
                           WHERE prod_id = %s or name = %s""",
                           (pd.name, pd.price, pd.quantity, pd.created_At,  pd.prod_id, pd.name))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error updating item in the database:", e)
            return False

    def deleteItem(self,prod_id:int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM products WHERE prod_id = %s", (prod_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error deleting item from the database:", e)
            return False

    def viewItems(self,flag:str):
        try:
            cursor = self.connection.cursor()
            if flag == 'v':
                cursor.execute("SELECT Prod_id,name,Price,Quantity,Created_At FROM products")
            elif flag == 'a':
                cursor.execute("SELECT Prod_id,name,Price,Quantity,Created_At FROM products WHERE Quantity < 3")         
            items = cursor.fetchall()
            cursor.close()
            return items
        except Exception as e:
            print("Error viewing items from the database:", e)
            return False
          

    def addSupplier(self,sd: supplierDataModel):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                           INSERT INTO suppliers (supplier_name, contact_info)
                           VALUES (%s, %s)""",
                           (sd.supplier_name, sd.contact_info))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Error adding supplier to the database:", e)
            return False