import tkinter as tk 
from tkinter import ttk,messagebox
from unicodedata import name
from db import * 
import os
import csv
from  datetime import datetime

class InventryApp:
    def __init__(self,root):
        self.root = root
        self.inventryMain()
        self.db = productData()
        self.pd = productDataModel(name="",catogory="", price=0.0, quantity=0,supplier="")
        self.sd = supplierDataModel(supplier_name="",contact_info="")

    def inventryMain(self):
        self.root.title("Inventry management")
        self.root.geometry("700x700")

        mainOptions = ttk.Frame(self.root,padding="15")
        mainOptions.pack(fill='both',expand=True)

        
        add_product_btn = ttk.Button(mainOptions,text="Add Product",command=self.addItem, padding=10)
        add_product_btn.grid(row=0, column=0, padx=10, pady=40, sticky='ew',ipady=20)
        del_product_btn = ttk.Button(mainOptions,text="Delete Product",command=self.deleteItem, padding=10)
        del_product_btn.grid(row=0, column=1, padx=10, pady=40, sticky='ew',ipady=20)
        upd_product_btn = ttk.Button(mainOptions,text="Update Product",command=self.updateItem,padding=10)
        upd_product_btn.grid(row=1, column=0, padx=10, pady=40, sticky='ew',ipady=20)
        add_supp_btn = ttk.Button(mainOptions,text="Add Supplier",command=self.addSupplier,padding=10)
        add_supp_btn.grid(row=1, column=1, padx=10, pady=40, sticky='ew',ipady=20)
        view_product_btn = ttk.Button(mainOptions,text="View products",command=self.viewProducts,padding=10)
        view_product_btn.grid(row=2, column=0, padx=10, pady=40, sticky='ew',ipady=20)
        alert_product_btn = ttk.Button(mainOptions,text="View Low stock products",command=self.alertProducts,padding=10)
        alert_product_btn.grid(row=2, column=1, padx=10, pady=40, sticky='ew',ipady=20)
        submit_btn = ttk.Button(mainOptions, text="Report", command=self.generateReport)
        submit_btn.grid(row=3, column=0, padx=10, pady=40, sticky='ew',ipady=20)

        mainOptions.columnconfigure(0,weight=1)
        mainOptions.columnconfigure(1,weight=1)
        mainOptions.rowconfigure(0,weight=1)
        mainOptions.rowconfigure(1,weight=1)

    def addItem(self):
        def submit():
            name = prod_name.get()
            price = prod_price.get()
            category = prod_category.get()
            quantity = quantity_entry.get()
            dataconvert = {}
            if  not name or not price or not quantity or not category:
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                price = float(price)
                quantity = int(quantity)    
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")
                return
            dataconvert["name"]=name
            dataconvert["price"]=price  
            dataconvert["category"]=category
            dataconvert["quantity"]=quantity
            
            self.pd = productDataModel(**dataconvert)
            met = self.db.addItem(self.pd)
        

            if met:
                messagebox.showinfo("Success", "Product added successfully.")
                addItemWindow.destroy()
            else:
                messagebox.showerror("Error", "Failed to add product.")

        addItemWindow = tk.Toplevel(self.root)
        addItemWindow.title("Add Product")
        addItemWindow.geometry("700x400")

        addItem_frame = ttk.Frame(addItemWindow, padding="15")
        addItem_frame.pack(fill='both', expand=True)

        prod_name = ttk.Label(addItem_frame, text="Product Name:")
        prod_name.grid(row=0, column=0,padx=10, pady=10, sticky='w')
        prod_name = ttk.Entry(addItem_frame)
        prod_name.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        prod_category = ttk.Label(addItem_frame, text="Category:")
        prod_category.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        prod_category = ttk.Entry(addItem_frame)
        prod_category.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        prod_price = ttk.Label(addItem_frame, text="Price:")
        prod_price.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        prod_price = ttk.Entry(addItem_frame)
        prod_price.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        quantity_label = ttk.Label(addItem_frame, text="Quantity:")
        quantity_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        quantity_entry = ttk.Entry(addItem_frame)
        quantity_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        submit_btn = ttk.Button(addItem_frame, text="Submit", command=submit)
        submit_btn.grid(row=5, column=0, pady=20)

        addItem_frame.columnconfigure(0, weight=1)
        addItem_frame.columnconfigure(1, weight=2)
        

        

    def deleteItem(self):
        def submit():
            prod_id = prod_id_entry.get().strip()
            if not prod_id:
                messagebox.showerror("Error", "Product ID is required.")
                return
            try:
                item_id = int(prod_id)
            except ValueError:
                messagebox.showerror("Error", "Product ID must be an integer.")
                return
            
            met  = self.db.deleteItem(prod_id)

            if met:
                messagebox.showinfo("Success", "Product deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete product.")

            deleteItemWindow.destroy()

        deleteItemWindow = tk.Toplevel(self.root)
        deleteItemWindow.title("Delete Product")
        deleteItemWindow.geometry("300x200")

        deleteItem_frame = ttk.Frame(deleteItemWindow, padding="15")
        deleteItem_frame.pack(fill='both', expand=True)

        prod_id_entry = ttk.Label(deleteItem_frame, text="Product ID:")
        prod_id_entry.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        prod_id_entry = ttk.Entry(deleteItem_frame)
        prod_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        submit_btn = ttk.Button(deleteItem_frame, text="Submit", command=submit)
        submit_btn.grid(row=1, column=0, columnspan=2, pady=20)
        

        # 

        deleteItem_frame.columnconfigure(0, weight=1)
        deleteItem_frame.columnconfigure(1, weight=2)

    def addSupplier(self):
        def submit():
            supplier_name = sup_name.get().strip()
            contact_info = supp_contact.get().strip()
            if not supplier_name or not contact_info:
                messagebox.showerror("Error", "All fields are required.")
                return
            convertdata = {}
            convertdata["supplier_name"]=supplier_name
            convertdata["contact_info"]=contact_info
            self.sd = supplierDataModel(**convertdata)
            met = self.db.addSupplier(self.sd)

            if met:
                messagebox.showinfo("Success", "Supplier added successfully.")
            else:
                messagebox.showerror("Error", "Failed to add supplier.")
            addSupplierWindow.destroy()

        addSupplierWindow = tk.Toplevel(self.root)
        addSupplierWindow.title("Add Supplier")
        addSupplierWindow.geometry("400x300")

        addSupplier_frame = ttk.Frame(addSupplierWindow, padding="15")
        addSupplier_frame.pack(fill='both', expand=True)

        sup_name = ttk.Label(addSupplier_frame, text="Supplier Name:")
        sup_name.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        sup_name = ttk.Entry(addSupplier_frame)
        sup_name.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        supp_contact = ttk.Label(addSupplier_frame, text="Contact Info:")
        supp_contact.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        supp_contact = ttk.Entry(addSupplier_frame)
        supp_contact.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        submit_btn = ttk.Button(addSupplier_frame, text="Submit", command=submit)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=20)    

        addSupplier_frame.columnconfigure(0, weight=1)
        addSupplier_frame.columnconfigure(1, weight=2)
    
    def viewProducts(self):
        viewProductsWindow = tk.Toplevel(self.root)
        viewProductsWindow.title("View Products")
        viewProductsWindow.geometry("2000x300")

        viewProducts_frame = ttk.Frame(viewProductsWindow, padding="15")
        viewProducts_frame.pack(fill='both', expand=True)

        columns = ("Prod_ID", "Name", "Price", "Quantity", "Created At")
        tree = ttk.Treeview(viewProducts_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')
        tree.pack(fill='both', expand=True)
        flag = 'v'
        products = self.db.viewItems(flag)
        if products:
            for product in products:
                tree.insert('', 'end', values=product)
        else:
            messagebox.showerror("Error", "Failed to retrieve products.")

        viewProducts_frame.columnconfigure(0, weight=1)
        viewProducts_frame.rowconfigure(0, weight=1)

    def updateItem(self):
        def submit():
            item_id = prod_id_entry.get().strip()
            name = prod_name_entry.get().strip()
            price = prod_price_entry.get().strip()
            quantity = quantity_entry.get().strip()
            category = prod_category_entry.get().strip()
            if not item_id or not name or not price or not quantity or not category:
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                item_id = int(item_id)
                price = float(price)
                quantity = int(quantity)    
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")
                return
            convertdata ={}
            convertdata["prod_id"]=item_id
            convertdata["name"]=name
            convertdata["price"]=price
            convertdata["quantity"]=quantity
            convertdata["category"]=category
            pd = productDataModel(**convertdata)
            met = self.db.updateItem(pd)
            if met:
                messagebox.showinfo("Success", "Product updated successfully.")
                updateItemWindow.destroy()
            else:
                messagebox.showerror("Error", "Failed to update product.")

        updateItemWindow = tk.Toplevel(self.root)
        updateItemWindow.title("Update Product")
        updateItemWindow.geometry("600x500")

        updateItem_frame = ttk.Frame(updateItemWindow, padding="15")
        updateItem_frame.pack(fill='both', expand=True)

        prod_name_entry = ttk.Label(updateItem_frame, text="Product Name:")
        prod_name_entry.grid(row=0, column=0, columnspan=2,padx=10, pady=10, sticky='w')
        prod_name_entry = ttk.Entry(updateItem_frame)
        prod_name_entry.grid(row=0, column=1,columnspan=2, padx=10, pady=10, sticky='ew')

        prod_category_entry = ttk.Label(updateItem_frame, text="Category:")
        prod_category_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        prod_category_entry = ttk.Entry(updateItem_frame)
        prod_category_entry.grid(row=1, column=1,columnspan=2, padx=10, pady=10, sticky='ew')

        prod_price_entry = ttk.Label(updateItem_frame, text="Price:")
        prod_price_entry.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        prod_price_entry = ttk.Entry(updateItem_frame)
        prod_price_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

        quantity_label = ttk.Label(updateItem_frame, text="Quantity:")
        quantity_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        quantity_entry = ttk.Entry(updateItem_frame)
        quantity_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

        prod_id_label = ttk.Label(updateItem_frame, text="Product Id:")
        prod_id_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        prod_id_entry = ttk.Entry(updateItem_frame)
        prod_id_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

        submit_btn = ttk.Button(updateItem_frame, text="Submit", command=submit)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=20)

        updateItem_frame.columnconfigure(0, weight=1)
        updateItem_frame.rowconfigure(1, weight=1)

    def alertProducts(self):
        alertProductsWindow = tk.Toplevel(self.root)
        alertProductsWindow.title("Low Stock Products")
        alertProductsWindow.geometry("2000x300")

        alertProducts_frame = ttk.Frame(alertProductsWindow, padding="15")
        alertProducts_frame.pack(fill='both', expand=True)

        columns = ("Prod_ID", "Name", "Price", "Quantity", "Created At")
        tree = ttk.Treeview(alertProducts_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')
        tree.pack(fill='both', expand=True)
        flag='a'
        products = self.db.viewItems(flag)
        if products:
            for product in products:
                tree.insert('', 'end', values=product)
        else:
            messagebox.showinfo("Info", "No low stock products found.")

        alertProducts_frame.columnconfigure(0, weight=1)
        alertProducts_frame.rowconfigure(0, weight=1)
    
    def generateReport(self):
        flag = 'v'
        products = self.db.viewItems(flag)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename= f"inventory_report_{timestamp}.csv"
        if products:
            with open(filename, 'w',  encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Product Name', 'Price', 'Quantity', 'Category'])
                for product in products:
                    writer.writerow([
                        product[0], 
                        product[1],  
                        product[2],  
                        product[3],  
                        product[4],     
                    ])
            
            print(f"Exported {len(products)} products to {filename}")
            return filename, len(products)



root = tk.Tk()
app = InventryApp(root)
root.mainloop()

